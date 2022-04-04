import pickle
from typing import Dict, List, Tuple

import pandas as pd
import lightgbm as lgb
import numpy as np

from easyai.abstracts import AbstractModelClass
from easyai.ml_modules import StringProcessingClass, CategoricalReplaceClass, SplitDataClass
from easyai.other_modules.UploaderClass import UploaderClass

class GBDTClass(AbstractModelClass):
    """
    Modelクラスを継承したGBDT用クラス
        コンストラクタ
        インスタンス変数に代入と特徴量作成用インスタンス生成

        Parameters
        ----------
        objective: str
            目的変数名

        original_path : str
            元データパス

        extension : str
            元データ拡張子

        task : str
            解きたい問題の種類(回帰など)
    """
    __TYPE = 'GBDT'
    __NEEDMISSING = False


    def make_instance(self):
        self.string_process = StringProcessingClass()
        self.categorical_process = CategoricalReplaceClass()
        self.split_process = SplitDataClass()

    def __init__(self, user_id, objective, original_path, task) -> None:
        super().__init__(user_id, objective, original_path, task)
        self.model = None

        #TODO: 決め打ち
        self.method = 'label-encoding'
        self.make_instance()

    def get_type():
        """
        このクラスのモデル種類を返す。
        """
        return GBDTClass.__TYPE

    def get_my_type(self):
        """
        このクラスのモデル種類を返す。
        """
        return GBDTClass.__TYPE

    def get_need_missing(self) -> bool:
        """
        このクラスは欠損値処理が必要かどうかを返す
        """
        return GBDTClass.__NEEDMISSING

    def make_auto_features(self):
        self.set_backup_df()
        self.categorical(self.method)
        self.df_cast_as_float32()

    def make_lgb_train_and_val_datatset(self, train_x, valid_x, train_y, valid_y) -> Tuple[lgb.Dataset, lgb.Dataset]:
        """
        lightgbmのデータセットを作成する

        Parameters
        ----------
        train_x : DataFrame
            trainの目的変数以外

        valid_x : DataFrame
            validationの目的変数以外
        
        train_y : DataFrame
            trainの目的変数

        valid_y : DataFrame
            validationの目的変数
        
        returns
        -------
        lgb_train: lightgbm.basic.Dataset
            lightgbmの学習データセット
        
        lgb_valid : lightgbm.basic.Dataset
            lightgbmの検証データセット
        """

        lgb_train = lgb.Dataset(train_x, train_y, free_raw_data=False)
        lgb_valid = lgb.Dataset(valid_x, valid_y)
        return lgb_train, lgb_valid

    # TODO: DBから取得
    def set_loss(self):
        """
        task : str
        nnを使用して解くタスクの種類
        'binary':二値分類
        'regression':回帰
        'multiclass':多クラス分類
        のどれかが格納される。
        """

        if self.task == 'binary':
            self.loss = 'binary_logloss'

        elif self.task == 'regression':
            self.loss = 'rmse'

        elif self.task == 'multiclass':
            self.loss = 'multi_logloss'


    # TODO: 決め打ち

    def set_lgb_params(self, max_depth=-1, learn_rate=0.1) -> None:
        """
        lightgbmのパラメータを設定する
        ※ここでのobjectiveはタスクの種類を示す。
        """
        self.db_values['max_depth'] = max_depth
        self.db_values['learn_rate'] = learn_rate


        if self.task == 'multiclass':
            classes = len([value for value in self.df[self.objective].unique() if str(value) != 'nan'])
            self.params = {'objective': self.task, 'num_classes': classes,
                            'metrics': self.loss, 'max_depth': max_depth, 'learning_rate' : learn_rate }
        else:
            self.params = {'objective': self.task,
                        'metrics': self.loss, 'max_depth': max_depth, 'learning_rate': learn_rate}


    # TODO: 決め打ち
    def set_round(self, round=5000, early_stopping_rounds=10):
        self.round = round
        self.db_values['num_round'] = round
        self.early_stopping_rounds = early_stopping_rounds
        self.db_values['early_stopping_rounds'] = early_stopping_rounds

    # TODO: 決め打ち
    def train_model(self, train, valid, params, rounds, early_stopping_rounds) -> dict:
        """
        lightgbmを使って学習する。

        Parameters
        ----------
        train : lightgbm.basic.Dataset
            学習データ
        valid : lightgbm.basic.Dataset
            検証データ
        params : dict
            lightgbmのパラメータ
        rounds : int
            epoch数
        """

        lgb_results = {}
        self.model = lgb.train(params, train, num_boost_round=rounds, valid_sets=[train, valid],
                                early_stopping_rounds=early_stopping_rounds, verbose_eval=10, evals_result=lgb_results)
        return lgb_results

    def lgb_show_result(self, train_data) -> None:
        """
        lightgbmの特徴量重要度を表とグラフで可視化する

        Parameters
        ----------
        train_data : df
            学習に使用したデータ(目的変数なし)
        """
        cols = list(train_data.columns)
        f_importance = np.array(self.model.feature_importance())
        f_importance = f_importance / np.sum(f_importance)  # 正規化(必要ない場合はコメントアウト)
        df_importance = pd.DataFrame({'feature': cols, 'importance': f_importance})
        df_importance = df_importance.sort_values(
            'importance', ascending=False)
        # print(df_importance)
        self.plot_data = df_importance

    

    def make_lgb_model(self):
        """
        モデルを訓練し、作成する。
        """
        self.db_values = {}

        self.set_loss()
        self.set_round()
        self.set_lgb_params()
        train_x, valid_x, train_y, valid_y = self.split_process.split(self.df, self.objective, self.valid_size, self.random_state)
        self.inserter.insert_DivisionData(
            random_state=self.random_state,
            test_size=self.valid_size,
            feature_value_obj=self.get_feature_obj()
        )
        lgb_train, lgb_valid = self.make_lgb_train_and_val_datatset(train_x ,valid_x, train_y, valid_y)
        history = self.train_model(
            lgb_train, lgb_valid, self.params, self.round, self.early_stopping_rounds)
        self.machine_learn_id = self.inserter.insert_MachineLearning(
            loss_value=history['training'][self.loss][-1],
            val_loss_value=history['valid_1'][self.loss][-1],
            loss_obj=self.selecter.select_loss_use_name(function_name=self.loss),
            feature_value_obj=self.get_feature_obj()
        )
        self.lgb_show_result(train_x)


    def save_model(self):
        """
        override 
        モデル保存
        """
        self.uploader.make_dir('model/' + str(self.user_id))
        fname = self.uploader.make_now_time_path()
        fpath = UploaderClass.ROOT + 'model/' + str(self.user_id) + '/' + fname + '.pkl'
        pickle.dump(self.model, open(fpath, 'wb'))

        self.model_id = self.inserter.insert_Models(
            path=fname,
            extension_obj=self.selecter.select_extension_use_name(extensions_name='pkl'),
            machine_learning_obj=self.selecter.select_machine_learning_use_index(id=self.machine_learn_id),
        )

        self.inserter.insert_GradientBoostingDecisionTree(
            model_obj=self.selecter.select_models_use_index(id=self.model_id),
            learn_rate=self.db_values['learn_rate'],
            max_depth=self.db_values['max_depth'],
            num_round=self.db_values['num_round'],
            early_round=self.db_values['early_stopping_rounds']
        )

    def model_evaluation(self):
        #TODO: 要実装 評価＆insert
        pass

    def auto_ml(self):
        self.make_auto_features()
        self.make_lgb_model()
        self.save_model()
        self.model_evaluation()

    # TODO: DBから取得
    def predict(self, predict_df):
        result = self.model.predict(predict_df)
        message = 'AIの予測評価が高いほどAIは正確に判断できていると考えています。'
        self.has_result = True
        if self.task == 'binary':
            ans = round(result[0])
            accuracy = (1-(abs(ans - result)))*100
            self.result = [
                '分類結果: '+ str(ans),
                'AIの予測評価:'+ str(accuracy)+'%',
                message
                ]
    
        elif self.task == 'regression':
            self.result = [
                '予測値: '+ str(result[0]),
                '',
                ''
                ]

        elif self.task == 'multiclass':
            ans_class = np.argmax(result[0])
            accuracy = result[0][ans_class]*100
            self.result = [
                'このデータが属するクラス: '+ str(ans_class),
                'AIの予測評価: ' + str(accuracy)+'%',
                message
                ] 

    def ensemble_predict(self, predict_df):
        self.result = self.model.predict(predict_df)[0]