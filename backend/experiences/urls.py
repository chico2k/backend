from django.urls import path

from experiences.api import \
    ExperienceListApi, \
    ExperienceDetailApi, \
    ExperienceUpdateApi, \
    ExperienceCreateApi, \
    ExperienceDeleteApi

app_name = "experiences"

urlpatterns = [

    path('', ExperienceListApi.as_view(), name="list"),
    path('<int:pk>/', ExperienceDetailApi.as_view(), name="detail"),
    path('create/', ExperienceCreateApi.as_view(), name="create"),
    path('<int:pk>/update', ExperienceUpdateApi.as_view(), name="update"),
    path('<int:pk>/delete', ExperienceDeleteApi.as_view(), name="delete"),
]
