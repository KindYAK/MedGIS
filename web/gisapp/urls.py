from django.urls import path
from .views import *

app_name = 'gisapp'

urlpatterns = [
    path('', GisView.as_view(), name="gis"),
]
