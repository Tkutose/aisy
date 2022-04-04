from django.urls.base import reverse_lazy
from easyai.views.base import ReplaceStringView
from easyai.forms import ReplaceStringForm


class FullReplaceStringView(ReplaceStringView):
    template_name = 'easyai/full/replace_string.html'
    success_url = reverse_lazy('easyai:full_missing_process')
    form_class = ReplaceStringForm

    def post(self, request):
        en_models = self.ml_controller.get_en_instance_all(self.user_id)
        for model in en_models.values():
            keys = [*request.POST.copy()]

            if 'replaces_col_name' in keys:
                replace_column = request.POST.getlist('replaces_col_name')
                replace_before = request.POST.getlist('replaces_before')
                replace_after = request.POST.getlist('replaces_after')
                for column, before, after in zip(replace_column, replace_before, replace_after):
                    model.replace_string(column, before, after)
            else:
                pass

            if 'deletes_col_name' in keys:
                delete_column = request.POST.getlist('deletes_col_name')
                delete_str = request.POST.getlist('deletes_str')
                for column, delete, in zip(delete_column, delete_str):
                    model.delete_string(column, delete)
            else:
                pass
        return super().post(self, request)
