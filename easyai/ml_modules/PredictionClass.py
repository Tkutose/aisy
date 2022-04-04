import numpy as np
import pandas as pd
from sqlalchemy import column
from easyai.ml_modules import (CategoricalReplaceClass, MissingProcessClass,
                                    SplitDataClass, StandardizationClass,
                                    StringProcessingClass)
from tensorflow.keras import models

from easyai.other_modules import SelectClass, UploaderClass
class PredictionClass():

    selecter = SelectClass()

    def make_instance(self):
        self.string_process = StringProcessingClass()
        self.missing_process = MissingProcessClass()
        self.categorical_process = CategoricalReplaceClass()
        self.standard_process = StandardizationClass()
        self.split_process = SplitDataClass()

    def __init__(self):
        self.df = None
        self.objective=''
        self.model_type=''
        self.task=''
        self.is_ensemble = False
        self.df_id = None
        self.has_id_colimn = False
        self.model_id = None
        self.model = None
        self.has_result = False
        self.result = None
        self.make_instance()

    def set_is_ensemble(self):
        self.is_ensemble =True

    def get_is_ensemble(self):
        return self.is_ensemble

    def set_df(self, df):
        self.df = df
        self.ensemble_df = {}

    def get_df(self):
        return self.df

    def set_ensemble_df(self, model_type):
        if self.is_ensemble:
            self.ensemble_df[model_type] = self.df.copy().astype('float32')
        else:
            pass

    def get_ensemble_df(self, model_type):
        return self.ensemble_df[model_type]

    def set_model_type(self, model_type):
        self.model_type = model_type

    def get_model_type(self):
        return self.model_type

    def set_objective(self, column_name):
        self.objective = column_name

    def get_objective(self):
        return self.objective

    def set_task(self, column_name):
        self.task = column_name

    def get_task(self):
        return self.task

    def set_df_index(self, column_name):
        self.df_id = column_name
        self.has_id_colimn = True
        self.df_id_column = self.df[column_name]

    def get_df_index(self):
        return self.df_id

    def set_model_id(self, id):
        self.model_id = id

    def get_model_id(self):
        return self.model_id

    def get_result(self):
        return self.result

    def delete_columns(self, delete_column_name):
        self.df = self.string_process.delete_one_column(
            self.get_df(), delete_column_name)

    def replace_string(self, column_name, before, after):
        self.df = self.string_process.replace_str_value(
            self.get_df(), column_name, before, after)

    def categorical_replace(self, column_name, before, after):
        self.df = self.string_process.replace_str_value(
            self.get_df(), column_name, before, after, is_regex=False)

    def fill_missing(self, column_name, value):
        self.df = self.missing_process.fill_value(
            self.get_df(), column_name, value)

    def df_cast_as_float32(self):
        self.df = self.df.astype('float32')
    
    def delete_missing(self):
        if self.model_type == 'GBDT':
            pass
        else:
            for column in self.df.columns.values:
                if self.df[column].isnull().sum() != 0:
                    mean = self.df[column].mean()
                    self.missing_process.fill_value(self.df, column, mean)

    def standard_use_train(self,train):
        if self.model_type == 'GBDT':
            pass
        else:
            train = train.drop(self.objective, axis=1)
            self.df = self.standard_process.standard_predict_data(train, self.df)

    def predict(self, model_path):
        if self.is_ensemble:
            self.ensemble_predict()

        elif self.model_type == 'NN':
            self.nn_predict(self.df, model_path)

        elif self.model_type == 'GBDT':
            self.gbdt_predict(self.df, model_path)
            
        elif self.model_type == 'RF':
            self.rf_predict(self.df, model_path)

        if self.task == 'multiclass':
            pass
        else:
            if self.has_id_colimn:
                    self.result[self.get_df_index()] = self.df_id_column
                    self.result = self.result.reindex(columns=[self.get_df_index(), self.objective])
        self.replace_result()

    def nn_predict(self, df, path):
        model = models.load_model(path)
        if self.task == 'multiclass':
            self.result = pd.DataFrame(model.predict(df))
        else:
            self.result = pd.DataFrame(model.predict(df), columns=[self.objective])

    def gbdt_predict(self, df, path):
        model = pd.read_pickle(path)
        if self.task == 'multiclass':
            self.result = pd.DataFrame(model.predict(df))
        else:
            self.result = pd.DataFrame(model.predict(df)[:,np.newaxis], columns=[self.objective])

    def rf_predict(self, df, path):
        model = pd.read_pickle(path)
        if self.task == 'multiclass':
            self.result = pd.DataFrame(model.predict(df))
        else:
            self.result = pd.DataFrame(model.predict(df), columns=[self.objective])

    def rf_ensemble_predict(self, df, path):
        model = pd.read_pickle(path)

        pre = model.predict(df)
        basis = model.predict_proba(df)
        result = []
        for index in range(len(pre)):
            ans = int(round(pre[index]))
            result.append(abs(basis[index][ans] - abs(ans-1)))

        if self.task == 'multiclass':
            self.result = pd.DataFrame(result)
        else:

            self.result = pd.DataFrame(result, columns=[self.objective])

    def ensemble_predict(self):
        main_model = self.selecter.select_model_info_use_index(self.model_id)
        en_id = main_model.ensemble_id
        user_id = main_model.user_id
        models = self.selecter.select_model_info_use_en_id(en_id)
        root = UploaderClass.ROOT + 'model/' + str(user_id) + '/'
        for model in models:
            model_obj = self.selecter.select_models_use_index(model.model_id)
            extension = self.selecter.select_extension_use_index(model_obj.extension.id).extensions_name
            path = root+ str(model_obj.path) + '.' + extension
            if model.model_type == 'NN':
                self.nn_predict(self.df ,path)
                nn_result = self.result

            elif model.model_type == 'GBDT':
                self.gbdt_predict(self.get_ensemble_df('GBDT'), path)
                gbdt_result = self.result

            elif model.model_type == 'RF':
                self.rf_ensemble_predict(self.get_ensemble_df('RF'), path)
                rf_result = self.result

        self.result = (nn_result + gbdt_result + rf_result) /3



    def replace_result(self):
        if self.task == 'binary':
            self.result[self.objective] = round(self.result[self.objective]).astype(int)
        elif self.task == 'regression':
            pass
        elif self.task == 'multiclass':
            ans = []
            for index, data in self.result.iterrows():
                ans.append(np.argmax(data))
            self.result = pd.DataFrame(ans, columns=[self.objective])
            if self.has_id_colimn:
                self.result[self.get_df_index()] = self.df_id_column
                self.result = self.result.reindex(columns=[self.get_df_index(), self.objective])