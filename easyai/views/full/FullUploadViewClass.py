import os
from django.urls import reverse_lazy
from easyai.views.base import UploadView


class FullUploadView(UploadView):
    template_name = 'easyai/common/upload.html'
    success_url = reverse_lazy('easyai:full_target_setting')

    def post(self, request):
        file = request.FILES['file']
        extension = os.path.splitext(file.name)[1]
        if self.extension_validate(extension):
            file_name = os.path.splitext(file.name)[0]
            extension = extension.replace('.', '')
            path = self.file_save(request, self.user_id)
            self.inserter.insert_OriginalData(
                path=path, file_name=file_name, extension_name=extension, user_id=self.user_id)
        return super().post(request)
