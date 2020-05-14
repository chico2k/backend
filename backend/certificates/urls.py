from django.urls import path

from certificates.api import \
    CertificateListAPI, \
    CertificateDetailAPI, \
    CertificateCreateAPI, \
    CertificateUpdateAPI, \
    CertificateDeleteAPI

app_name = "certificates"

urlpatterns = [
    path('', CertificateListAPI.as_view(), name="list"),
    path('<int:pk>/', CertificateDetailAPI.as_view(), name="detail"),
    path('create/', CertificateCreateAPI.as_view(), name="create"),
    path('<int:pk>/update/', CertificateUpdateAPI.as_view(), name="update"),
    path('<int:pk>/delete/', CertificateDeleteAPI.as_view(), name="delete"),

]
