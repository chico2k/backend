import pytest
from mixer.backend.django import mixer
from certificates.models import Certificate
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from certificates.selectors import \
    get_list_certificate, \
    get_detail_certificate
from rest_framework.exceptions import NotFound
User = get_user_model()


def test_certificates_list_success():
    """
    Test Certificates shown for Profile ID
    """
    user1 = mixer.blend(User)
    user2 = mixer.blend(User)
    mixer.blend(Certificate, profile=user1.profile)
    mixer.blend(Certificate, profile=user1.profile)
    mixer.blend(Certificate,
                profile=user1.profile,
                is_published=False)
    mixer.blend(Certificate, profile=user2.profile)
    result = get_list_certificate(profile=user1.profile.id)

    assert len(result) == 2


def test_certificates_list_null():
    """
    Test return empty list when Profile has no Certificates
    """
    res = get_list_certificate(profile=2)

    assert len(res) == 0


def test_certificates_detail_success():
    """
    Test that only Certificate for specific ID is shown
    """
    user1 = mixer.blend(User)
    certificate = mixer.blend(Certificate, profile=user1.profile)
    mixer.blend(Certificate, profile=user1.profile)
    result = get_detail_certificate(id=certificate.id)
    assert result == certificate
