from typing import Dict, List
import matplotlib
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
matplotlib.use('Agg')


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from easyai.abstracts import AbstractModelClass
from easyai.ml_modules import (CategoricalReplaceClass, MissingProcessClass,
                                    SplitDataClass, StandardizationClass,
                                    StringProcessingClass)
from easyai.other_modules import UploaderClass
from keras.utils import np_utils
from tensorflow import keras
from tensorflow.keras import layers, models


class NNClass(AbstractModelClass):
    """
    Modelクラスを継承したニューラルネットワーク用クラス
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
    __TYPE = 'NN'
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
        self.use_standard = False
        self.no_standard_df = None

        #TODO: 決め打ち
        self.method = 'label-encoding'
        self.make_instance()

    def get_df(self):
        if self.use_standard:
            return self.no_standard_df
        else :
            return self.df

    def get_type():
        """
        このクラスのモデル種類を返す。
        """
        return NNClass.__TYPE

    def get_my_type(self):
        """
        このクラスのモデル種類を返す。
        """
        return NNClass.__TYPE

    def get_need_missing(self) -> bool:
        """
        このクラスは欠損値処理が必要かどうかを返す
        """
        return NNClass.__NEEDMISSING

    def get_metrics(self) -> str:
        return self.metrics

    def make_auto_features(self) -> None:
        """
        自動化する部分の特徴量作成
        """
        self.set_backup_df()
        self.categorical(self.method)
        self.df_cast_as_float32()
        self.standard()



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
    def set_epoch_and_batch_size(self, epoch=15, batch_size=128):
        self.epoch = epoch
        self.db_values['epoch'] = epoch
        self.batch_size = batch_size
        self.db_values['batch_size'] = batch_size


    def build_model(self, train_x, train_y) -> None:
        """
        metricsとlossを設定し、NNモデルを構築して、インスタンス変数に格納する。

        Parameters
        ----------
        train_x : DataFrame
            trainの目的変数以外

        train_y : DataFrame
            trainの目的変数
        """
        self.set_metrics_and_loss()
        self.set_epoch_and_batch_size()
        
        h_activation = 'relu'
        self.db_values['hidden_activation'] = h_activation
        h_units = 64
        self.db_values['units'] = h_units
        num_layers = 1
        self.db_values['num_layers'] = num_layers
        is_batch = True
        self.db_values['is_batch'] = 1 if is_batch else 0
        is_early = False
        self.db_values['is_early'] = 1 if is_early else 0
        is_dropout = False
        self.db_values['is_dropout'] = 1 if is_dropout else 0

        model = models.Sequential()
        # input
        model.add(layers.Dense(h_units, activation=h_activation,
                            input_shape=[len(train_x.keys())]))
        if is_batch:
            model.add(layers.BatchNormalization())

        # hidden
        for i in range(num_layers):
            model.add(layers.Dense(h_units, activation=h_activation))
            if is_batch:
                model.add(layers.BatchNormalization())


        # output
        if self.task == 'binary':
            model.add(layers.Dense(1, activation='sigmoid'))
            self.db_values['output_activation'] = 'sigmoid'
        
        elif self.task == 'regression':
            model.add(layers.Dense(1))
            self.db_values['output_activation'] = 'linear'
        
        elif self.task == 'multiclass':
            unit = len(train_y.unique())
            model.add(layers.Dense(unit, activation='softmax'))
            self.db_values['output_activation'] = 'softmax'

        l_r = 0.01
        self.db_values['learn_rate'] = l_r
        self.db_values['optimizer'] = 'Adam'

        # compile
        model.compile(loss=self.loss,
                    optimizer=keras.optimizers.Adam(learning_rate=l_r),
                    metrics=[self.metrics])
        self.model = model

    
    def draw_history_graph(self, history) -> None:
        """
        NNモデルの学習結果をグラフ化する

        Parameters
        ----------
        history : keras.callbacks.History
            model.fitの返り値(学習結果)
        
        """
        result = pd.DataFrame(history.history)
        self.plot_data = result



    def train_model(self, train_x, valid_x, train_y, valid_y, is_result_graph=True) -> pd.DataFrame:
        """
        NNモデルを学習して返す

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
        
        is_result_graph : bool
            結果のグラフを描画するかどうか  
            default:True    
        """
        if self.task == 'multiclass':
            train_y = np_utils.to_categorical(train_y)
            valid_y = np_utils.to_categorical(valid_y)
        else:
            pass

        history = self.model.fit(
            train_x,
            train_y,
            batch_size=self.batch_size,
            epochs=self.epoch,
            validation_data=(valid_x, valid_y)
        )
        if is_result_graph == True:
            self.draw_history_graph(history)
            pass
        return pd.DataFrame(history.history)


    def make_nn_model(self):
        """
        モデルを訓練し、作成する。
        """

        self.db_values = {}
        train_x, valid_x, train_y, valid_y = self.split_process.split(self.df, self.objective, self.valid_size, self.random_state) 
        self.inserter.insert_DivisionData(
            random_state=self.random_state,
            test_size=self.valid_size,
            feature_value_obj=self.get_feature_obj()
        )

        self.build_model(train_x, train_y)
        history = self.train_model(train_x, valid_x, train_y, valid_y)
        
        self.machine_learn_id = self.inserter.insert_MachineLearning(
            loss_value=history.iloc[-1]['loss'],
            val_loss_value=history.iloc[-1]['val_loss'],
            loss_obj=self.selecter.select_loss_use_name(function_name=self.loss),
            feature_value_obj=self.get_feature_obj()
        )


    def get_model(self):
        """
        NNモデルを返す
        """
        return self.model

    
    def save_model(self):
        """
        override 
        モデル保存
        TODO:idをmachine_learnnigに変更
        """

        self.uploader.make_dir('model/' + str(self.user_id))
        fname = self.uploader.make_now_time_path()
        fpath = UploaderClass.ROOT + 'model/' + str(self.user_id) + '/' + fname + '.h5'
        self.model.save(fpath)

        self.model_id = self.inserter.insert_Models(
            path=fname,
            extension_obj=self.selecter.select_extension_use_name(
                extensions_name='h5'),
            machine_learning_obj=self.selecter.select_machine_learning_use_index(
                id=self.machine_learn_id),
        )

        #TODO: is_early関連のmin_delta,patientは使用していないためinsertせず(default値)
        self.inserter.insert_no_early_NeuralNetwork(
            model_obj=self.selecter.select_models_use_index(id=self.model_id),
            num_layers=self.db_values['num_layers'],
            units=self.db_values['units'],
            hidden_activation_obj=self.selecter.select_activation_use_name(self.db_values['hidden_activation']),
            optimizer_obj=self.selecter.select_optimizer_use_name(self.db_values['optimizer']),
            is_batchnormalization=self.db_values['is_batch'],
            is_early_stopping=self.db_values['is_early'],
            is_dropout=self.db_values['is_dropout'],
            epoch=self.db_values['epoch'],
            batch_size=self.db_values['batch_size'],
            learn_rate=self.db_values['learn_rate'],
            output_activation_obj=self.selecter.select_activation_use_name(self.db_values['output_activation'])
        )

    def model_evaluation(self):
        #TODO: 要実装 評価＆insert
        pass


    def auto_ml(self):
        self.make_auto_features()
        self.make_nn_model()
        self.save_model()
        self.model_evaluation()


    def predict(self, predict_df):
        predict_df = self.standard_process.standard_predict_data(self.no_standard_df, predict_df)

        result = self.model.predict(predict_df)
        message = 'AIの予測評価が高いほどAIは正確に判断できていると考えています。'
        self.has_result = True
        if self.task == 'binary':
            ans = round(result[0][0])
            accuracy = (1-(abs(ans - result)))*100
            self.result = [
                '分類結果: ' + str(ans),
                'AIの予測評価:' + str(accuracy[0][0])+'%',
                message
            ]

        elif self.task == 'regression':
            self.result = [
                '予測値: ' + str(result[0][0]),
                '',
                ''
            ]

        elif self.task == 'multiclass':
            ans_class = np.argmax(result[0][0])
            accuracy = result[0][ans_class]*100
            self.result = [
                'このデータが属するクラス: ' + str(ans_class),
                'AIの予測評価: ' + str(accuracy)+'%',
                message
            ]
        
    def ensemble_predict(self, predict_df):
        self.result = self.model.predict(predict_df)[0][0]