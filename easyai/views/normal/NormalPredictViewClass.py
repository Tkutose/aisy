from easyai.views.base import PredictView
from easyai.forms import PredictForm
from django.urls import reverse_lazy
from pandas import DataFrame
import matplotlib
matplotlib.use('Agg')



class NormalPredictView(PredictView):
    template_name = 'easyai/common/predict.html'
    form_class = PredictForm
    success_url = reverse_lazy('easyai:normal_predict')


    def post(self, request):
        self.predict_dict.clear()
        model = self.ml_controller.get_ml_instance(self.user_id)
        keys = [*request.POST.copy()]
        keys.remove('csrfmiddlewaretoken')
        predict_value = [[]]
        for key in keys:
            predict_value[0].append(float(request.POST[key]))
            self.predict_dict[key] = request.POST[key]
        predict_df = DataFrame(predict_value, columns=keys)
        model.predict(predict_df)
        self.replace_predict_dict()
        return super().post(self, request)
