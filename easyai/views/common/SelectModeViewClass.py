from django.views import generic

class SelectModeView(generic.TemplateView):
    template_name = 'easyai/common/select_mode.html'
