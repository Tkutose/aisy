from django.shortcuts import redirect
from django.urls import reverse_lazy
from easyai.forms import PredictForm

from easyai.views.base import MLCompleteView


class NormalMLCompleteView(MLCompleteView):
    template_name = 'easyai/full/auto_ml.html'
    success_url = reverse_lazy('easyai:normal_predict')
    form_class = PredictForm
    
    def get(self, request):
        model = self.ml_controller.get_ml_instance(self.user_id)
        model.auto_ml()
        return redirect('easyai:normal_predict', permanent=True)

