from django.urls import path
from .api import ReviewListApi, ReviewCreateApi, ReviewResponseCreateApi

app_name = "reviews"

urlpatterns = [
    path('', ReviewListApi.as_view(), name="list"),
    path('create/', ReviewCreateApi.as_view(), name="create"),
    path('<int:review_id>/response/', ReviewResponseCreateApi.as_view(), name="create-response")
]
