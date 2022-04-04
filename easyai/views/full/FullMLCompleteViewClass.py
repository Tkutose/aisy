from django.shortcuts import redirect
from django.urls import reverse_lazy
from easyai.forms import PredictForm
from easyai.other_modules import InsertClass, SelectClass

from easyai.views.base import MLCompleteView


class FullMLCompleteView(MLCompleteView):
    template_name = 'easyai/full/auto_ml.html'
    success_url = reverse_lazy('easyai:full_predict')
    form_class = PredictForm
    inserter = InsertClass()
    selecter = SelectClass()

    def get(self, request):
        en_models = self.ml_controller.get_en_instance_all(self.user_id)
        for model in en_models.values():
            model.auto_ml()
        self.insert_ensemble()
        return redirect('easyai:full_predict', permanent=True)


    def insert_ensemble(self):
        #TODO: 決め打ち
        method_obj = self.selecter.select_ensemble_method_use_name('mean')
        ensemble_id = self.inserter.insert_EnsembleEvaluations(ensemble_method_obj=method_obj)
        ensemble_obj = self.selecter.select_ensemble_evaluations_use_index(ensemble_id)
        en_models = self.ml_controller.get_en_instance_all(self.user_id)
        for model in en_models.values():
            model_obj = self.selecter.select_models_use_index(id = model.get_model_id())
            
            self.inserter.insert_EnsembleCompositions(
                model_obj=model_obj,
                ensemble_obj=ensemble_obj
            )
