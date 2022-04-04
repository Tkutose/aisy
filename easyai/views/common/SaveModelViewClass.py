from django.http import FileResponse
from django.views.generic.base import View
from easyai.other_modules import MLControllClass

class SaveModelView(View):
    ml_controller = MLControllClass()
    # TODO: 決め打ち
    user_id = 1

    def get(self, request, *args, **kwargs):
        model = self.ml_controller.get_ml_instance(self.user_id)
        path = model.get_model_path()
        fname = model.get_download_model_name()
        return FileResponse(open(path, "rb"), as_attachment=True, filename=fname)
        

