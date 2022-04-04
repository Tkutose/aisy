from django.urls.base import reverse_lazy
from easyai.forms import DeleteStringForm
from easyai.views.base import DeleteStringView

class FullDeleteStringView(DeleteStringView):
    template_name = 'easyai/full/delete_string.html'
    form_class = DeleteStringForm
    success_url = reverse_lazy('easyai:full_replace_string')

    def post(self, request):
        delete_columns = request.POST.getlist('column_names')
        en_models = self.ml_controller.get_en_instance_all(self.user_id)
        for en_model in en_models.values():
            en_model.delete_columns(delete_columns)
        return super().post(self, request)
