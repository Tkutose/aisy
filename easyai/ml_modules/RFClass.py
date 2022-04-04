import pickle
from typing import Dict, List

import matplotlib
import numpy as np
import pandas as pd
from easyai.abstracts import AbstractModelClass
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.model_selection import train_test_split

matplotlib.use('Agg')

from easyai.ml_modules import (CategoricalReplaceClass, MissingProcessClass,
                                SplitDataClass, StandardizationClass,
                                StringProcessingClass)
from easyai.other_modules import UploaderClass


class RFClass(AbstractModelClass):
    """
    Modelクラスを継承したランダムフォレスト用クラス
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
    __TYPE = 'RF'
    __NEEDMISSING = True

    def make_instance(self):
        self.string_process = StringProcessingClass()
        self.missing_process = MissingProcessClass()
        self.categorical_process = CategoricalReplaceClass()
        self.standard_process = StandardizationClass()
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
        return RFClass.__TYPE

    def get_my_type(self):
        """
        このクラスのモデル種類を返す。
        """
        return RFClass.__TYPE

    def get_need_missing(self) -> bool:
        """
        このクラスは欠損値処理が必要かどうかを返す
        """
        return RFClass.__NEEDMISSING

    def get_metrics(self) -> str:
        return self.metrics


    def make_auto_features(self) -> None:
        """
        自動化する部分の特徴量作成
        """
        self.set_backup_df()
        self.categorical(self.method)
        self.df_cast_as_float32()

    # TODO: DBから取得

    def set_metrics_and_loss(self):
        """
        task : str
        nnを使用して解くタスクの種類
        'binary':二値分類
        'regression':回帰
        'multiclass':多クラス分類
        のどれかが格納される。
        """

        if self.task == 'binary':
            self.metrics = 'accuracy'
            self.loss = 'binary_crossentropy'

        elif self.task == 'regression':
            self.metrics = 'mae'
            self.loss = 'mse'

        elif self.task == 'multiclass':
            self.metrics = 'accuracy'
            self.loss = 'categorical_crossentropy'

    # TODO: 決め打ち

    def set_params(self, random_state=71, max_depth=10, max_features=3, min_samples_split=5, n_estimators=20):
        self.random_state = random_state
        self.db_values['random_state'] = random_state

        self.max_depth = max_depth
        self.db_values['max_depth'] = max_depth

        self.max_features = max_features
        self.db_values['max_features'] = max_features

        self.min_samples_split = min_samples_split
        self.db_values['min_samples_split'] = min_samples_split
        
        self.n_estimators= n_estimators
        self.db_values['n_estimators'] = n_estimators
        

    def build_model(self) -> None:
        """
        taskごとに別のインスタンスを生成し、self.modelに格納する。
        """
        self.set_metrics_and_loss()
        self.set_params()

        if self.task == 'binary' or self.task == 'multiclass':
            rf = RFC(
                    random_state=self.random_state,
                    max_depth=self.max_depth,
                    max_features=self.max_features,
                    min_samples_split=self.min_samples_split,
                    n_estimators=self.n_estimators
                    )

        elif self.task == 'regression':
            rf = RFR(
                    random_state=self.random_state,
                    max_depth=self.max_depth,
                    max_features=self.max_features,
                    min_samples_split=self.min_samples_split,
                    n_estimators=self.n_estimators)

        self.model = rf


    def train_model(self, train_x, train_y, is_result_graph=True) -> pd.DataFrame:
        """
        NNモデルを学習して返す

        Parameters
        ----------
        train_x : DataFrame
            trainの目的変数以外
        train_y : DataFrame
            trainの目的変数

        """

        self.model.fit(
            train_x,
            train_y,
        )

    def make_rf_model(self):
        """
        モデルを訓練し、作成する。
        """

        self.db_values = {}
        train_x = self.get_df()
        train_y = train_x.pop(self.objective)

        self.build_model()
        history = self.train_model(train_x, train_y)

        self.machine_learn_id = self.inserter.insert_MachineLearning(
            loss_value=-1,
            val_loss_value=-1,
            loss_obj=self.selecter.select_loss_use_name(
                function_name=self.loss),
            feature_value_obj=self.get_feature_obj()
        )

    def get_model(self):
        """
        RFモデルを返す
        """
        return self.model

    def save_model(self):
        """
        override 
        モデル保存
        """

        self.uploader.make_dir('model/' + str(self.user_id))
        fname = self.uploader.make_now_time_path()
        fpath = UploaderClass.ROOT + 'model/' + \
            str(self.user_id) + '/' + fname + '.pkl'
        pickle.dump(self.model, open(fpath, 'wb'))

        self.model_id = self.inserter.insert_Models(
            path=fname,
            extension_obj=self.selecter.select_extension_use_name(
                extensions_name='pkl'),
            machine_learning_obj=self.selecter.select_machine_learning_use_index(
                id=self.machine_learn_id),
        )

        self.inserter.insert_RandomForest(
            model_obj=self.selecter.select_models_use_index(id=self.model_id),
            random_state = self.db_values['random_state'],
            max_depth=self.db_values['max_depth'],
            max_features=self.db_values['max_features'],
            min_samples_split=self.db_values['min_samples_split'],
            n_estimators= self.db_values['n_estimators']
        )

    def model_evaluation(self):
        #TODO: 要実装 評価＆insert
        pass

    def auto_ml(self):
        self.make_auto_features()
        self.make_rf_model()
        self.save_model()
        self.model_evaluation()


    def predict(self, predict_df):
        result = self.model.predict(predict_df)
        message = 'AIの予測評価が高いほどAIは正確に判断できていると考えています。'
        self.has_result = True
        if self.task == 'binary':
            basis = self.model.predict_proba(predict_df)
            ans = round(result[0])
            accuracy = basis[0][ans]*100
            self.result = [
                '分類結果: ' + str(ans),
                'AIの予測評価:' + str(accuracy)+'%',
                message
            ]

        elif self.task == 'regression':
            self.result = [
                '予測値: ' + str(result[0]),
                '',
                ''
            ]

        elif self.task == 'multiclass':
            basis = self.model.predict_proba(predict_df)
            ans_class = np.argmax(result[0])
            accuracy = basis[0][ans_class]*100
            self.result = [
                'このデータが属するクラス: ' + str(ans_class),
                'AIの予測評価: ' + str(accuracy)+'%',
                message
            ]

    def ensemble_predict(self, predict_df):
        if self.task == 'binary':
            result = self.model.predict(predict_df)
            basis = self.model.predict_proba(predict_df)
            ans = round(result[0])
            self.result = abs(basis[0][ans] - abs(ans-1))

        else:
            self.result = self.model.predict(predict_df)
