from django.urls.base import reverse_lazy
import pandas as pd
from easyai.forms import EasyTargetSettingForm
from easyai.views.base import TargetSettingView


class EasyTargetSettingView(TargetSettingView):
    template_name = 'easyai/easy/target_setting.html'
    form_class = EasyTargetSettingForm
    success_url = reverse_lazy('easyai:easy_delete_string')

    def post(self, request):
        path = self.uploader.ROOT + self.uploader.get_last_upload_path(self.user_id)
        df = pd.read_csv(path)

        objective = request.POST['objective']
        model_type = 'GBDT'

        #TODO: 要改善 task自動判別(最低20行/多クラスは20クラスまで)
        if len(df[objective].unique()) <= 2:
            task = 'binary'
        elif len(df[objective].unique()) <= 20:
            task = 'multiclass'
        elif len(df[objective].unique()) > 20:
            task= 'regression'

        path = self.uploader.get_last_upload_path(self.user_id)
        self.make_ml_instance(model_type, objective, self.uploader.ROOT+path, task)
        return super().post(self, request)