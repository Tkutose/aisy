from django.urls import path
from easyai.views.common import SavePredictionView, SelectModeView, SaveDataFrameView, IndexView, SaveModelView
from easyai.views.prediction import SelectMakeModelView, PredictionDataUploadView, PredictionView, PredictionSettingView
from easyai.views.easy import EasyUploadView, EasyDeleteStringView, EasyMLCompleteView, EasyPredictView, EasyTargetSettingView
from easyai.views.normal import NormalUploadView, NormalDeleteStringView, NormalReplaceStringView, NormalMissingProcessView, NormalMLCompleteView, NormalPredictView, NormalTargetSettingView
from easyai.views.full import FullUploadView, FullDeleteStringView, FullReplaceStringView, FullMissingProcessView, FullMLCompleteView, FullPredictView, FullTargetSettingView
app_name = 'easyai'


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('mode', SelectModeView.as_view(), name="select_mode"),

    path('use/model', SelectMakeModelView.as_view(), name="select_make_model"),
    path('use/<model_id>/upload', PredictionDataUploadView.as_view(), name="prediction_upload"),
    path('use/<model_id>/setting', PredictionSettingView.as_view(), name="prediction_setting"),
    path('use/<model_id>/predict', PredictionView.as_view(), name="prediction"),
    
    
    path('easy/upload', EasyUploadView.as_view(), name="easy_upload"),
    path('easy/target_setting', EasyTargetSettingView.as_view(), name="easy_target_setting"),
    path('easy/delete_string', EasyDeleteStringView.as_view(), name="easy_delete_string"),
    path('easy/auto_ml', EasyMLCompleteView.as_view(), name="easy_auto_ml"),
    path('easy/predict', EasyPredictView.as_view(), name="easy_predict"),

    path('normal/upload', NormalUploadView.as_view(), name="normal_upload"),
    path('normal/target_setting', NormalTargetSettingView.as_view(), name="normal_target_setting"),
    path('normal/delete_string', NormalDeleteStringView.as_view(), name="normal_delete_string"),
    path('normal/replace_string', NormalReplaceStringView.as_view(), name="normal_replace_string"),
    path('normal/missing_process', NormalMissingProcessView.as_view(), name="normal_missing_process"),
    path('normal/auto_ml', NormalMLCompleteView.as_view(), name="normal_auto_ml"),
    path('normal/predict', NormalPredictView.as_view(), name="normal_predict"),

    path('full/upload', FullUploadView.as_view(), name="full_upload"),
    path('full/target_setting', FullTargetSettingView.as_view(), name="full_target_setting"),
    path('full/delete_string', FullDeleteStringView.as_view(), name="full_delete_string"),
    path('full/replace_string', FullReplaceStringView.as_view(), name="full_replace_string"),
    path('full/missing_process', FullMissingProcessView.as_view(), name="full_missing_process"),
    path('full/auto_ml', FullMLCompleteView.as_view(), name="full_auto_ml"),
    path('full/predict', FullPredictView.as_view(), name="full_predict"),

    path('model/download', SaveModelView.as_view(), name='model_download'),
    path('data/download', SaveDataFrameView.as_view(), name='data_download'),
    path('predict/download', SavePredictionView.as_view(), name='predict_download')
]
