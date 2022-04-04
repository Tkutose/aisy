from easyai.views.base import PredictView
from easyai.forms import PredictForm
from django.urls import reverse_lazy
from pandas import DataFrame
import numpy as np
import matplotlib
matplotlib.use('Agg')



class FullPredictView(PredictView):
    template_name = 'easyai/full/predict.html'
    form_class = PredictForm
    success_url = reverse_lazy('easyai:full_predict')

    def post(self, request):
        en_models = self.ml_controller.get_en_instance_all(self.user_id)
        for model in en_models.values():
            self.predict_dict.clear()
            keys = [*request.POST.copy()]
            keys.remove('csrfmiddlewaretoken')
            predict_value = [[]]
            for key in keys:
                predict_value[0].append(float(request.POST[key]))
                self.predict_dict[key] = request.POST[key]
            predict_df = DataFrame(predict_value, columns=keys)
            model.ensemble_predict(predict_df)
            self.replace_predict_dict()
        self.ensemble_mean()
        return super().post(self, request)

    def ensemble_mean(self):
        sum_value = 0
        self.ensemble_result.clear()
        en_models = self.ml_controller.get_en_instance_all(self.user_id)
        main_model = self.ml_controller.get_ml_instance(self.user_id)
        for model in en_models.values():
            sum_value += model.get_result()
            self.ensemble_result.append(
                str(model.get_my_type())+': ' + str(model.get_result()))
        mean = sum_value / len(en_models)

        message = 'AIの予測評価が高いほどAIは正確に判断できていると考えています。'
        if main_model.task == 'binary':
            ans = round(mean)
            accuracy = (1-(abs(ans - mean)))*100
            result = [
                '分類結果: ' + str(ans),
                'AIの予測評価:' + str(accuracy)+'%',
                message
            ]

        elif main_model.task == 'regression':
            result = [
                '予測値: ' + str(mean),
                '',
                ''
            ]

        elif main_model.task == 'multiclass':
            ans_class = np.argmax(mean)
            accuracy = mean[0][ans_class]*100
            result = [
                'このデータが属するクラス: ' + str(ans_class),
                'AIの予測評価: ' + str(accuracy)+'%',
                message
            ]

        main_model.set_result(result)

    def get_context_data(self, **kwargs):
        """
        オーバーライド
        """
        context = super().get_context_data(**kwargs)
        try:
            context['ensemble'] = self.ensemble_result
        except AttributeError as e:
            pass
        return context
