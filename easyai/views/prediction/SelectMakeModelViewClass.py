import datetime
from django.views import generic
from easyai.other_modules import SelectClass

class SelectMakeModelView(generic.TemplateView):
    template_name = 'easyai/prediction/select_make_model.html'
    selecter = SelectClass()
    # TODO: 決め打ち
    user_id = 1

    def get(self, request):
        return super().get(self, request)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = self.model_replace(self.get_models())
        return context

    def get_models(self):
        model = self.selecter.select_models_by_user_use_user_id(id=self.user_id)
        return model

    def time_to_date(self, models):
        """
        models内のpathを作成日時に置き換えて返す
        """
        for model in models:
            model.time = datetime.datetime.fromtimestamp(float(model.model_path) / 1000000000)
        return models

    def change_aisy_mode(self, model_type) -> str:
        if model_type == 'GBDT':
            return 'お手軽モード'
        else :
            return '本格モード'
    
    def delete_ensemble_duplicate(self, models):
        """
        アンサンブルしたモデルは代表1つのみにして返す
        """
        unique = []
        duplicates = []
        for model in models:
            if model.ensemble_id in unique:
                duplicates.append(model.id)
            else:
                if model.ensemble_id != None: unique.append(model.ensemble_id)
                model.mode = self.change_aisy_mode(model.model_type)
                    
        models = [model for model in models if model.id not in duplicates]
        return models

    def model_replace(self, models):
        models = self.time_to_date(models)
        return self.delete_ensemble_duplicate(models)