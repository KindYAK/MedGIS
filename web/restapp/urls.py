from django.conf.urls import include, url
from rest_framework import routers

from restapp.views import *

router = routers.DefaultRouter()
router.register("range_documents", RangeDocumentsViewSet, basename="range_documents")

app_name = 'restapp'

urlpatterns = [
    url('', include(router.urls)),
]
