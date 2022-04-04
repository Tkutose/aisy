from django import forms
from django.urls import reverse_lazy
from easyai.forms import PredictSettingForm
from django.views.generic.edit import FormView
from easyai.other_modules import MLControllClass

class PredictionSettingView(FormView):
    template_name = 'easyai/prediction/predict_setting.html'
    form_class = PredictSettingForm
    # TODO: 決め打ち
    user_id = 1
    ml_controller = MLControllClass()

    def get_context_data(self, **kwargs):
        """
        formとアップロードされたcsv取得
        """
        context = super().get_context_data(**kwargs)
        predict = self.ml_controller.get_predict_instance(self.user_id)
        df = predict.get_df()
        choices = [(' ', '該当なし')]
        for column in df.columns.values:
            choices.append((column, column))

        form = self.get_form()
        form.fields['id'] = forms.ChoiceField(
            choices=choices,
            widget=forms.widgets.Select(
                attrs={'class': 'm-1 border-gray-800 focus:outline-none border-none p-2 rounded-md border-r border-gray-300'}),
            label='')

        context = {
            'df': df,
            'form': form
        }
        return context

    def post(self, request, model_id):
        predict = self.ml_controller.get_predict_instance(self.user_id)
        id_column = request.POST['id']
        if id_column != ' ':
            predict.set_df_index(id_column)

        self.success_url = reverse_lazy('easyai:prediction',
                                        kwargs={'model_id': model_id},)
        return super().post(request)
