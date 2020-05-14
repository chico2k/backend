from django.urls import path
from django.conf.urls import include


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('auth/jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
