from django.urls.base import reverse_lazy
from easyai.views.base import ReplaceStringView
from easyai.forms import ReplaceStringForm


class NormalReplaceStringView(ReplaceStringView):
    template_name = 'easyai/full/replace_string.html'
    form_class = ReplaceStringForm

    def post(self, request):
        model = self.ml_controller.get_ml_instance(self.user_id)        
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

        if model.get_need_missing():
            self.success_url = reverse_lazy('easyai:normal_missing_process')
        else:
            self.success_url = reverse_lazy('easyai:normal_auto_ml')
        return super().post(self, request)
