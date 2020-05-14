from certificates.models import Certificate
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound


def get_list_certificate(*, profile):
    """
    Get all Certificates for Profile Raise 404 if not found
    """
    certificate = Certificate.objects.filter(
        profile__id=profile,
        is_published=True)
    return certificate


def get_detail_certificate(*, id):
    """
    Get Detail Certificate for a Profile
    """
    return get_object_or_404(Certificate, id=id)
