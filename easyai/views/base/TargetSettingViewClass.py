from django import forms
from django.urls.base import reverse_lazy
from django.views.generic.edit import FormView


import pandas as pd

from easyai.other_modules import UploaderClass, MLControllClass

class TargetSettingView(FormView):
    uploader = UploaderClass()
    ml_controller = MLControllClass()
    # TODO: 決め打ち
    user_id = 1


    def get_context_data(self, **kwargs):
        """
        formとアップロードされたcsv取得
        """
        context = super().get_context_data(**kwargs)

        path = self.uploader.ROOT + self.uploader.get_last_upload_path(self.user_id)
        df = pd.read_csv(path)

        form = self.get_form()
        form.fields['objective'] = forms.ChoiceField(
            choices=[(column, column) for column in df.columns.values],
            widget=forms.widgets.Select(attrs={'class': 'm-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300'}),
            label='')            


        context = {
            'df' : df,
            'form': form
        }
        return context

    def make_ml_instance(self, model_type, objective, path, task):
        self.ml_controller.init_ml_instance(self.user_id, model_type, objective, path, task)