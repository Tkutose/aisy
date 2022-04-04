from django.views import generic
import pandas as pd

from easyai.other_modules import MLControllClass, SelectClass, UploaderClass

class PredictionView(generic.TemplateView):
    template_name = 'easyai/prediction/predict.html'
    # TODO: 決め打ち
    user_id = 1
    selecter = SelectClass()
    ml_controller = MLControllClass()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        predict = self.ml_controller.get_predict_instance(self.user_id)
        context['df'] = predict.get_result()
        return context

    def get(self, request, model_id):
        self.ml_controller.get_predict_instance(self.user_id)
        self.model_feature_process(model_id)
        self.predict(model_id)
        return super().get(request)

    def model_feature_process(self, model_id):
        predict = self.ml_controller.get_predict_instance(self.user_id)
        self.delete_string_process(predict, model_id)
        self.replace_string_process(predict, model_id)
        self.categorical_process(predict, model_id)
        predict.set_ensemble_df('GBDT')
        self.missing_process(predict, model_id)
        predict.delete_missing()
        predict.set_ensemble_df('RF')
        predict.df_cast_as_float32()
        print(predict.get_df())
        print(predict.get_df().info())
        self.standard(predict, model_id)

    def delete_string_process(self, predict, model_id):
        delete_strings = self.selecter.select_done_delete_string_use_index(model_id)
        for delete_string in delete_strings:
            if delete_string.delete_column == None:
                continue
            predict.delete_columns(delete_string.delete_column)

    def replace_string_process(self, predict, model_id):
        replace_strings = self.selecter.select_done_replace_string_use_index(model_id)
        for replace_string in replace_strings:
            if replace_string.after_str == None: replace_string.after = '' 
            if replace_string.column_name == None:
                continue

            predict.replace_string(
                replace_string.column_name, replace_string.before_str, replace_string.after_str)

    def categorical_process(self, predict, model_id):
        categoricals = self.selecter.select_done_categorical_use_index(model_id)
        for categorical in categoricals:
            if categorical.after_str == None: categorical.after = ''
            if categorical.column_name == None: continue    
            predict.categorical_replace(
                categorical.column_name, categorical.before_str, float(categorical.after_str))

    def missing_process(self, predict, model_id):
        missings = self.selecter.select_done_missing_use_index(model_id)
        for missing in missings:
            if missing.column_name == None: continue
            predict.fill_missing(missing.column_name, missing.fill_str)

    def standard(self, predict, model_id):
        root = UploaderClass.ROOT
        model_info = self.selecter.select_model_info_use_index(model_id)
        path = root + 'data/' + str(model_info.user_id) + '/' + str(model_info.original_path) + '.csv' 
        train = pd.read_csv(path)
        predict.standard_use_train(train)

    def predict(self, model_id):
        model = self.selecter.select_models_use_index(model_id)
        extension = self.selecter.select_extension_use_index(
            model.extension.id).extensions_name
        user_id = self.selecter.select_model_info_use_index(model_id).user_id
        path = UploaderClass.ROOT + 'model/' + str(user_id) + '/' + str(model.path) + '.' + str(extension)
        predict = self.ml_controller.get_predict_instance(self.user_id)
        predict.predict(path)
