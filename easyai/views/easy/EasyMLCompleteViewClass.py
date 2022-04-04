from django.shortcuts import redirect
from django.urls import reverse_lazy
from easyai.forms import PredictForm
from easyai.views.base import MLCompleteView


class EasyMLCompleteView(MLCompleteView):

    template_name = 'easyai/easy/auto_ml.html'
    form_class = PredictForm

    def get(self, request):
        model = self.ml_controller.get_ml_instance(self.user_id)
        model.auto_ml()
        return redirect('easyai:easy_predict', permanent=True)

