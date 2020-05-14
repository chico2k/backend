from django.urls import path

from .api import \
    LocationGeocoderAPI, \
    LocationCreateApi

app_name = "locations"

urlpatterns = [

    path('', LocationGeocoderAPI.as_view(), name="list"),
    path('create/', LocationCreateApi.as_view(), name="create"),
]
