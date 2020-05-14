from django.urls import path, include
from profiles.api import \
    ProfileListApi,\
    ProfileDetailApi, \
    ProfileUpdateApi

app_name = "profiles"

urlpatterns = [
    path('', ProfileListApi.as_view(), name="list"),
    path('<int:profile_id>', ProfileDetailApi.as_view(), name="detail"),
    path('<int:profile_id>/update', ProfileUpdateApi.as_view(), name="update"),

    path('<int:profile_id>/sports/', include('sports.urls')),
    path('<int:profile_id>/reviews/', include('reviews.urls')),
    path('<int:profile_id>/experiences/', include('experiences.urls')),
    path('<int:profile_id>/certificates/', include('certificates.urls')),
]
