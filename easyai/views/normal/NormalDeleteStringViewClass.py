from django.urls.base import reverse_lazy
from easyai.forms import DeleteStringForm
from easyai.views.base import DeleteStringView

class NormalDeleteStringView(DeleteStringView):
    template_name = 'easyai/full/delete_string.html'
    form_class = DeleteStringForm
    success_url = reverse_lazy('easyai:normal_replace_string')

    def post(self, request):
        delete_columns = request.POST.getlist('column_names')
        model = self.ml_controller.get_ml_instance(self.user_id)
        model.delete_columns(delete_columns)
        return super().post(self, request)
