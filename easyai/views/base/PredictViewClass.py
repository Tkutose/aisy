import base64
import io
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from pandas import DataFrame
from easyai.ml_modules import NNClass, GBDTClass, RFClass
from easyai.other_modules import MLControllClass
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django import forms

class PredictView(FormView):
    ml_controller = MLControllClass()
    predict_dict = {}
    ensemble_result = []
    # TODO: 決め打ち
    user_id = 1


    def get_context_data(self, **kwargs):
        model = self.ml_controller.get_ml_instance(self.user_id)
        if model.get_my_type() == GBDTClass.get_type():
            self.gbdt_plot(model.get_graph_data())
        elif model.get_my_type() == NNClass.get_type():
            self.nn_plot(model.get_graph_data(), model.get_metrics())
        elif model.get_my_type() == RFClass.get_type():
            self.rf_plot(model.get_df(), model.get_model())
        
        graph = self.get_image()
        context = super().get_context_data(**kwargs)
        form = self.make_form()
        context['form'] = form
        context['graph'] = graph
        context['has_result'] = model.get_has_result()
        context['result'] = model.get_result()[0]
        context['accuracy'] = model.get_result()[1]
        context['message'] = model.get_result()[2]
        context['predict_value'] = self.predict_dict
        return context

    def replace_predict_dict(self):
        """
        表示する値逆カテゴリ変換し、わかりやすくする
        """
        model = self.ml_controller.get_ml_instance(self.user_id)
        categorical_dict = model.get_categorical()
        is_categorical_column = [*categorical_dict.keys()]
        for column, value in self.predict_dict.items():
            if column in is_categorical_column:
                self.predict_dict[column] = categorical_dict[column][float(value)]


    def gbdt_plot(self, data) -> None:        
        n_features = len(data)
        data_plot = data.sort_values('importance')
        f_importance_plot = data_plot['importance'].values
        plt.clf()
        plt.barh(range(n_features), f_importance_plot, align='center', color='gray')

        # 特徴量の取得
        cols_plot = data_plot['feature'].values
        plt.yticks(np.arange(n_features), cols_plot)
        plt.xlabel('Feature importance')
        plt.ylabel('Feature')

    def nn_plot(self, data, metrics):
        plt.clf()
        data[[metrics, 'val_'+metrics]].plot()


    def rf_plot(self, data, rf):
        fea_rf_imp = pd.DataFrame({'imp': rf.feature_importances_, 'col': data.columns.values})
        fea_rf_imp = fea_rf_imp.sort_values(by='imp', ascending=True)
        n_features = len( fea_rf_imp['col'])

        plt.clf()
        plt.barh(range(n_features), fea_rf_imp['imp'].values, align='center', color='gray')
        cols_plot = fea_rf_imp['col'].values
        plt.yticks(np.arange(n_features), cols_plot)
        plt.xlabel('Feature importance')
        plt.ylabel('Feature')


    def get_image(self):
        buffer = io.BytesIO()
        plt.savefig(buffer, format='svg', bbox_inches='tight')
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        buffer.close()
        return graph


    def make_form(self):
        model = self.ml_controller.get_ml_instance(self.user_id)
        df = model.get_df()
        categorical_dict = model.get_categorical()
        is_categorical_column = [*categorical_dict.keys()]

        form = self.get_form()
        for column in df.columns.values:
            if column in is_categorical_column:
                form.fields[column] = forms.ChoiceField(
                    # カテゴリ変数変換した値を元の値として表示(見た目のみ)
                    choices=[(value, categorical_dict[column][value]) if str(value)!='nan' else (value, 'データなし') for value in np.sort(df[column].unique())],
                    widget=forms.widgets.Select(attrs={'class': 'm-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300'})
                    )
            else:
                form.fields[column] = forms.DecimalField(widget=forms.widgets.NumberInput(
                    attrs={'class': 'm-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300'}))
        return form

