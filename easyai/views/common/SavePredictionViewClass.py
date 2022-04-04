from django.http import HttpResponse
from django.views.generic.base import View
from easyai.other_modules import MLControllClass
import pandas as pd

class SavePredictionView(View):
    ml_controller = MLControllClass()
    # TODO: 決め打ち
    user_id = 1

    def get(self, request, *args, **kwargs):
        prediction = self.ml_controller.get_predict_instance(self.user_id)
        df = prediction.get_result()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=predict.csv'
        df.to_csv(path_or_buf=response, index=False)
        
        return response