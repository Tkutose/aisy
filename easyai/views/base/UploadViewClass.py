import os
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from easyai.forms import UploadFileForm
from easyai.other_modules import InsertClass, UploaderClass


class UploadView(FormView):
    form_class = UploadFileForm

    inserter = InsertClass()
    uploader = UploaderClass()
    # TODO: 決め打ち
    user_id = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context = {
            'form': form,
        }
        return context

    def extension_validate(self, extension):
        if not extension.lower() in UploadFileForm.VALID_EXTENSIONS:
            return False
        return True

    def file_save(self, request, user):
        self.uploader.make_dir('data/' + str(user))
        fname = self.uploader.make_now_time_path()
        fpath = 'data/' + str(user) + '/' + fname + '.csv'
        updata = request.FILES.get('file')
        self.uploader.seve_as_csv(user, fpath, updata)
        return fname

    def tmp_file_save(self, request):
            updata = request.FILES.get('file')
            # self.uploader.seve_as_csv(user, fpath, updata)
