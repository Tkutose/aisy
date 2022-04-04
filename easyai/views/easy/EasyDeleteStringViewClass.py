from django import forms
from django.urls.base import reverse_lazy
from easyai.forms import DeleteStringForm
from easyai.views.base import DeleteStringView

class EasyDeleteStringView(DeleteStringView):
    success_url = reverse_lazy('easyai:easy_auto_ml')
    template_name = 'easyai/easy/delete_string.html'
    form_class = DeleteStringForm

    def post(self, request):
        delete_columns = request.POST.getlist('column_names')
        model = self.ml_controller.get_ml_instance(self.user_id)
        model.delete_columns(delete_columns)
        return super().post(self, request)
