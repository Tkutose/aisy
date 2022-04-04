from django import forms
from django.urls.base import reverse_lazy
from django.views.generic.edit import FormView

from easyai.other_modules import UploaderClass, MLControllClass

class DeleteStringView(FormView):
    uploader = UploaderClass()
    ml_controller = MLControllClass()
    # TODO: 決め打ち
    user_id = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.ml_controller.get_ml_instance(self.user_id)
        df = model.get_df()
        columns_list = df.columns.values.tolist()
        recommend_list = model.get_recommend_delete_column_names()
        form = self.make_form(
            list = self.remove_objective(columns_list, model.get_objective()),
            recommend_list=self.remove_objective(recommend_list, model.get_objective()),
        )
        context['df'] = df
        context['form'] = form
        return context

    def remove_objective(self, list, objective):
        for item in list:
            if item == objective:
                list.remove(objective)
        return list

    def make_form(self, list, recommend_list):
        """
        listの列名から目的変数を除外したチェックボックスを表示させ、
        recommend_listの列名にチェックを付けてformを作成する。
        """

        form = self.get_form()
        choices = []
        for column_name in list:
            choices.append((column_name, column_name) )
        form.fields['column_names'] = forms.MultipleChoiceField(
                                        widget=forms.CheckboxSelectMultiple,
                                        choices=choices,
                                        initial=recommend_list,
                                        label=''
                                        )
        
        return form