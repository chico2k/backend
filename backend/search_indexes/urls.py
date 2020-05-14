from django.urls import path

from .api import \
    ElasticSearchMultiAPI, \
    ElasticSearchSingleAPI

app_name = "elastic"

urlpatterns = [
    path('<str:index>/_msearch', ElasticSearchMultiAPI.as_view(), name="list"),
    path('<str:index>/_search', ElasticSearchSingleAPI  .as_view(), name="list"),
]
