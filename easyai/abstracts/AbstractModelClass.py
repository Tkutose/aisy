from abc import ABCMeta, abstractmethod
import pandas as pd
from typing import Dict, List
import base64
import io
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

from sqlalchemy import column

from easyai.other_modules import InsertClass, SelectClass
from easyai.other_modules.UploaderClass import UploaderClass

class AbstractModelClass(metaclass=ABCMeta):
    """
    モデル用の基底抽象クラス
        コンストラクタ
        インスタンス変数に代入のみを行う。

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

    inserter = InsertClass()
    selecter = SelectClass()
    uploader = UploaderClass()

    def __init__(self, user_id, objective, original_path, task) -> None:
        self.user_id = user_id
        self.objective = objective
        self.path = original_path
        self.task = task
        self.set_df()
        self.backup_df = None
        self.id_name = ''
        self.valid_size = 0.33
        self.random_state = 71
        self.plot_data = None
        self.is_ensemble = False
        
        self.has_result = False
        self.result = ['', '', '']

        self.feature_ids = None
        self.insert_feature_values()

    def insert_feature_values(self):
        id = self.inserter.insert_FeatureValues(
            original_obj=self.selecter.select_original_use_index(self.inserter.get_original_id(self.user_id)),
            objective=self.objective, 
            model_type_obj=self.selecter.select_model_types_use_type_name(self.get_my_type()), 
            task_obj=self.selecter.select_task_use_name(self.task)
            )
        self.set_feature_id(id)

    def set_df(self) -> None:
        path = self.path
        df = pd.read_csv(path)
        self.df = df

    def get_df(self) -> pd.DataFrame:
        return self.df

    def set_backup_df(self):
        self.backup_df = self.df

    def get_before_df(self):
        """
        直近の変更前のdfを返す
        """
        return self.backup_df

    def get_string_column_names(self) -> List[str]:
        return self.string_process.get_string_column_names(self.df)

    def get_recommend_delete_column_names(self) -> List[str]:
        return self.string_process.get_recommend_delete_columns(self.df)

    def delete_columns(self, delete_columns) -> None:
        self.set_backup_df()
        if type(delete_columns) == str:
            self.df = self.string_process.delete_one_column(
                self.df, delete_columns)
        else:
            self.df = self.string_process.delete_any_column(
                self.df, delete_columns)
        self.inserter.insert_DeleteString(
            feature_obj=self.get_feature_obj(),
            delete_list=delete_columns)
        self.update_csv()

    def replace_string(self, column, before, after):
        self.set_backup_df()
        self.df = self.string_process.replace_str_value(self.df, column, before, after)
        self.inserter.insert_ReplaceString(
            column_name=column,
            before=before,
            after=after,
            feature_obj=self.get_feature_obj()
        )
        self.update_csv()

    def delete_string(self, column, value):
        self.set_backup_df()
        self.df = self.string_process.delete_one_str_value(self.df, column, value)
        self.inserter.insert_ReplaceString(
            column_name=column,
            before=value, 
            after='',
            feature_obj=self.get_feature_obj(),
            regex=True)
        self.update_csv()

# TODO:DBから引用
    def categorical(self, method):
        if method == 'label-encoding':
            self.label_encoding(method)
        else:
            pass
        self.update_csv()


    def label_encoding(self, method):
        categorical_list = self.categorical_process.get_isnot_number_column_name(self.get_df())
        feature_obj = self.get_feature_obj()
        method_obj = self.selecter.select_categorical_method_use_name(method_name=method)
        for column in categorical_list:
            self.df = self.categorical_process.label_encoding(self.get_df(), column)
            for history in self.categorical_process.get_history():
                self.inserter.insert_CategoricalTransformation(
                    column=column,
                    before=history['before'],
                    after=history['after'],
                    feature_obj=feature_obj,
                    categorical_method_obj=method_obj
                )

    def df_cast_as_float32(self):
        self.df = self.df.astype('float32')


    def update_csv(self):
        """
        特徴量を更新する。(更新先はoriginal_data記載のパス)
        アンサンブルの材料として使用する場合は更新しない。
        """
        if self.is_ensemble:
            pass
        else:
            self.set_backup_df()
            self.df.to_csv(self.path, index=False)

    def get_categorical(self):
        """
        {
            列名1: {カテゴリ変換後の値1: 変換前の値1, カテゴリ変換後の値2: 変換前の値2}...,
            列名2: {カテゴリ変換後の値1: 変換前の値1, カテゴリ変換後の値2: 変換前の値2}...,
        }
        """
        categorical_dict = {}
        categorical = self.selecter.select_categorical_transformation_use_feature_id(self.get_feature_id())
        for item in categorical:
            categorical_dict[item.column_name] = {}
        for item in categorical:
            categorical_dict[item.column_name].update(
                {float(item.after_value) : item.before_value} 
                )
        return categorical_dict

    def get_missing_columns(self) -> Dict:
        return self.missing_process.get_missing_columns(self.df)

    def get_not_missing_columns(self) -> Dict:
        return self.missing_process.get_delete_columns(self.df)

    def fill_missing(self, col_name, value, method) -> None:
        """
        欠損値を埋める
        """
        self.set_backup_df()
        self.df = self.missing_process.fill_value(self.df, col_name, value)
        self.inserter.insert_MissingProcessing(
                missing_method_obj=self.selecter.select_missing_method_use_name(method),
                column_name=col_name,
                value=value,
                feature_obj=self.get_feature_obj()
            )
        self.update_csv()

    def standard(self):
        self.no_standard_df = self.df
        self.use_standard = True
        self.df = self.standard_process.standard_without_objective(self.get_df(),self.objective)
        self.inserter.insert_Standardization(
            is_standardization=1,
            feature_obj=self.get_feature_obj()
        )


    def get_model_path(self):
        model_obj = self.selecter.select_models_use_index(self.model_id)
        path = model_obj.path
        extension = self.selecter.select_extension_use_index(model_obj.extension.id).extensions_name
        # return '../static/easyai/model/' + str(self.user_id) + '/'+ path +'.'+ extension
        return self.uploader.ROOT + 'model/' + str(self.user_id) + '/'+ path +'.'+ extension

    def get_download_model_name(self):
        id = self.inserter.get_original_id(self.user_id)
        model_obj = self.selecter.select_models_use_index(self.model_id)
        extension = self.selecter.select_extension_use_index(model_obj.extension.id).extensions_name
        return self.selecter.select_original_use_index(id).file_name + '.'+ extension

    def get_original_name(self):
        id = self.inserter.get_original_id(self.user_id)
        name = self.selecter.select_original_use_index(id).file_name
        return name+'.csv'
    
    @abstractmethod
    def get_type():
        """
        abstract
        このクラスのモデル種類を返す。
        """
        raise NotImplementedError()

    def get_my_type(self):
        """
        abstract
        このクラスのモデル種類を返す。
        """
        raise NotImplementedError()

    @abstractmethod
    def save_model(self, path):
        """
        abstract
        完成したモデルを保存する。
        """
        raise NotImplementedError()
    
    @abstractmethod
    def make_instance(self):
        """
        abstract
        特徴量作成に必要なインスタンスを生成する。
        """
        raise NotImplementedError()

    @abstractmethod
    def auto_ml(self):
        """
        abstract
        自動化する部分を一括で呼び出す。
        具体的な内容は継承先で定義。
        """
        raise NotImplementedError()


    @abstractmethod
    def make_auto_features(self):
        """
        abstract
        特徴量作成のうち、自動化したものをまとめて呼び出す。
        具体的な内容は継承先で定義。
        """
        raise NotImplementedError()


    def get_objective(self):
        return self.objective

    def get_original_path(self):
        return self.path

    def set_feature_id(self, id):
        self.feature_id = id

    def get_feature_id(self):
        return self.feature_id

    def get_feature_obj(self):
        return self.selecter.select_feature_value_use_index(self.get_feature_id())

    def get_graph_data(self):
        return self.plot_data

    def get_has_result(self):
        return self.has_result

    def get_model_id(self):
        return self.model_id

    def set_result(self, result):
        self.has_result = True
        self.result = result

    def get_result(self):
        """
        [0]に結果
        [1]に信頼度(str)
        (ただし、回帰のみ空の文字列)
        """
        return self.result
