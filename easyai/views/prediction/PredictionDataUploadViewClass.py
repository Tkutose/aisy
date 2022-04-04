from django.urls import reverse_lazy
from easyai.other_modules import MLControllClass, SelectClass
from easyai.views.base import UploadView
import pandas as pd


class PredictionDataUploadView(UploadView):
    template_name = 'easyai/prediction/upload_prediction.html'
    # TODO: 決め打ち
    user_id = 1
    ml_controller = MLControllClass()
    selecter = SelectClass()
    

    def post(self, request, model_id):
        file = request.FILES['file']

        self.ml_controller.set_predict_instance(self.user_id)
        predict = self.ml_controller.get_predict_instance(self.user_id)
        learn_plan = self.selecter.select_learn_plan_use_index(id=model_id)
        model_info = self.selecter.select_model_info_use_index(id=model_id)
        predict.set_objective(learn_plan.objective)
        predict.set_task(learn_plan.task)
        predict.set_model_type(model_info.model_type)
        predict.set_model_id(model_id)
        if model_info.ensemble_id != None:
            predict.set_is_ensemble()

        df = pd.read_csv(file.temporary_file_path())
        predict.set_df(df)

        self.success_url = reverse_lazy('easyai:prediction_setting',
                                        kwargs={'model_id': model_id},)
        return super().post(request)