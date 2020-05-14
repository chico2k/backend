from django.urls import path

from .api import \
    SportListApi, \
    SportCreateApi, \
    SportDetailApi, \
    SportUpdateApi, \
    SportDeleteApi,\
    SporttypeAvailableToAdd

app_name = "sports"

urlpatterns = [

    path('', SportListApi.as_view(), name="list"),
    path('create/', SportCreateApi.as_view(), name="create"),
    path('sporttype/', SporttypeAvailableToAdd.as_view(), name="list_sporttype"),
    path('<int:pk>/', SportDetailApi.as_view(), name="detail"),
    path('<int:pk>/update/', SportUpdateApi.as_view(), name="update"),
    path('<int:pk>/delete/', SportDeleteApi.as_view(), name="delete"),
]
