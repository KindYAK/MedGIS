from django.views.generic import TemplateView

from medgis.settings import YANDEX_MAP_API_KEY


class GisView(TemplateView):
    template_name = "gisapp/gis.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yandex_map_api_key'] = YANDEX_MAP_API_KEY
        return context
