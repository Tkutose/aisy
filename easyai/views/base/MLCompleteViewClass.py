from django.shortcuts import redirect
import numpy as np
from django import forms
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from easyai.forms import PredictForm
from easyai.other_modules import MLControllClass


class MLCompleteView(FormView):
    ml_controller = MLControllClass()
    # TODO: 決め打ち
    user_id = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.make_form()
        context['form'] = form
        return context

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
                    choices=[(value, categorical_dict[column][value]) if str(value)!='nan' else (value, 'データなし') for value in np.sort(df[column].unique())]
                    )
            else:
                form.fields[column] = forms.DecimalField()
        return form


    def get(self, request):
        return redirect('easyai:predict', permanent=True)

