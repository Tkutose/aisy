from django.shortcuts import redirect
from django.urls import reverse_lazy
from easyai.forms import MissingProcessForm
from easyai.views.base import MissingProcessView

class NormalMissingProcessView(MissingProcessView):
    template_name = 'easyai/full/missing_processing.html'
    success_url = reverse_lazy('easyai:normal_auto_ml')
    form_class = MissingProcessForm

    def post(self, request):
        model = self.ml_controller.get_ml_instance(self.user_id)
        keys = [*request.POST.copy()]
        keys.remove('csrfmiddlewaretoken')
        for key in keys:
            column_name = key.replace('missing_', '').replace('delete_', '')
            value = request.POST[key].split('_',1)[0]
            method = request.POST[key].split('_',1)[1]
            model.fill_missing(column_name, value, method)
        return super().post(self, request)

    def get(self, request):
        model = self.ml_controller.get_ml_instance(self.user_id)
        missing = model.get_missing_columns()
        if (len(model.get_missing_columns()) == 0) and (len(model.get_not_missing_columns()) == 0):
            return redirect('easyai:full_auto_ml', permanent=True)
        else:
            return super().get(self, request)