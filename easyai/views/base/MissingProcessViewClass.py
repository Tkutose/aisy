from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from easyai.forms import MissingProcessForm
from django import forms
from easyai.other_modules import MLControllClass, InsertClass

class MissingProcessView(FormView):

    # TODO: 決め打ち
    user_id = 1
    ml_controller = MLControllClass()
    inserter = InsertClass()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = self.ml_controller.get_ml_instance(self.user_id)
        df = model.get_df()
        form = self.make_form(model.get_missing_columns(), model.get_not_missing_columns())
        context['form'] = form
        context['df'] = df
        return context

    def make_choices(self, value):
        """
        get_missing_columnsやget_not_missing_columnsで取得してきたdictを
        formsで扱えるchoicesの形にして返す
        """
        choices = [('','選択してください')]
        eng_dict = {'mean': '平均値', 'median': '中央値', 'mode': '最頻値'}
        for v_key, v_value in value.items():
            if v_key == 'mode':
                for mode_value in v_value:
                    choices.append(
                        (str(mode_value)+'_'+str(v_key), str(mode_value)+' ('+str(eng_dict[v_key]+')')))
            else :
                choices.append(
                    (str(v_value)+'_'+str(v_key), str(v_value)+' ('+str(eng_dict[v_key])+')'))
        return choices

    def make_form(self, missing_dict, delete_dict):
        self.has_missing = False
        self.has_delete = False
        
        form = self.get_form()
        for key in missing_dict.keys():
            self.has_missing = True
            form.fields['missing_'+str(key)] = forms.ChoiceField(
                choices=self.make_choices(missing_dict[key]),
                label=str(key),
                widget=forms.widgets.Select(attrs={'class': 'm-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300'})
                    )

        for key in delete_dict.keys():
            self.has_delete = True
            form.fields['delete_'+str(key)] = forms.ChoiceField(
                choices=self.make_choices(delete_dict[key]),
                label=str(key),
                widget=forms.widgets.Select(attrs={'class': 'm-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300'})
                )
        
        return form
