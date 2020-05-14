import pytest
import os
from django.core.exceptions import ValidationError
from unittest import mock
from django.core.files import File
from certificates.models import Certificate
from django.contrib.auth import get_user_model
User = get_user_model()


def test_certificates_string_correct(create_test_user):
    """
    Test Experience String
    """
    user1 = create_test_user()
    certificate = Certificate.objects.create(
        profile=user1.profile,
        title="Test Title",
        description="A description",
        organization="A Organization",
        completion_date="2020-01-01",
        is_published=True
    )
    assert str(certificate) == f'{certificate.profile}: {certificate.title}'


def test_certificate_file_types_ok(create_test_user):
    """
    Test that JPG, JPEG can be uploaded successfully
    """

    user = create_test_user()
    jpg_file = 'test/files/JPG.jpg'
    Certificate.objects.create(
        profile=user.profile,
        title="Test Title",
        description="A description",
        organization="A Organization",
        completion_date="2020-01-01",
        document=jpg_file,
        is_published=True
    )

    jpeg_file = 'test/files/JPEG.jpeg'
    Certificate.objects.create(
        profile=user.profile,
        title="Test Title",
        description="A description",
        organization="A Organization",
        completion_date="2020-01-01",
        document=jpeg_file,
        is_published=True
    )

    res = Certificate.objects.filter(profile=user.profile)
    assert len(res) == 2


def test_certificate_file_types_not_ok(create_test_user):
    """
    Test that fake Files cannot be upload
    """
    user = create_test_user()

    with pytest.raises(ValidationError):
        fake_jpg_file = 'test/files/FAKE_JPG.jpg'
        Certificate.objects.create(
            profile=user.profile,
            title="Test Title",
            description="A description",
            organization="A Organization",
            completion_date="2020-01-01",
            document=fake_jpg_file,
            is_published=True
        )

    assert ValidationError
