from django.urls.base import reverse_lazy
from django.views.generic.edit import FormView
from django import forms

from easyai.other_modules import InsertClass, MLControllClass


class ReplaceStringView(FormView):
    
    # TODO: 決め打ち
    user_id = 1
    ml_controller = MLControllClass()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.ml_controller.get_ml_instance(self.user_id)
        df = model.get_df()
        context['form'] = self.make_form(df.columns.values)
        context['df'] = df
        return context

    def make_form(self, list):
        """
        列名を取得し、ドロップダウンとしてformに追加
        """

        form = self.get_form()
        choices = [('','選択してください')]
        for column_name in list:
            choices.append((column_name, column_name) )
        form.fields['column_names'] = forms.ChoiceField(choices=choices, show_hidden_initial=True, label='列名',
                                                        widget=forms.widgets.Select(attrs={'class': 'bg-gray-100 m-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300',
                                                                                                'id':'js-column'}))
        form.fields['before_string']= forms.CharField(required=False, label='置き換え前',
                                                        widget=forms.widgets.TextInput(attrs={'class':'bg-gray-100 m-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300',
                                                                                                'id': 'js-replace-before'}))
        form.fields['after_string'] = forms.CharField(required=False, label='置き換え後',
                                                        widget=forms.widgets.TextInput(attrs={'class': 'bg-gray-100 m-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300',
                                                                                                'id': 'js-replace-after'}))
        form.fields['delete_string'] = forms.CharField(required=False, label='削除する文字列',
                                                        widget=forms.widgets.TextInput(attrs={'class': 'hidden bg-gray-100 m-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300',
                                                                                                'id': 'js-delete-string'}))
        return form
