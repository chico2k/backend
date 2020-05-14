from certificates.models import Certificate
from certificates.services import \
    add_certificate, \
    update_certificate, \
    delete_certificate
import pytest
from django.core.exceptions import ValidationError
from main.messages.messages import Errors
from mixer.backend.django import mixer


def test_certificates_add_success(create_test_user, tmpdir):
    """
    Test Certificate added to Profile
    """
    user = create_test_user()

    jpg_file = 'test/files/JPG.jpg'
    new_certificate = add_certificate(
        user=user,
        profile_id=user.profile.id,
        title="A Title",
        description="A description",
        organization="A Organization",
        document=jpg_file,
        completion_date="2020-01-01")

    new_certificate.save()

    res = Certificate.objects.filter(profile=user.profile)
    assert len(res) == 1

def test_certificates_add_success_required_fields(create_test_user):
    """
    Test Certificate added to Profile
    """
    user = create_test_user()

    new_certificate = add_certificate(
        user=user,
        profile_id=user.profile.id,
        title="A Title",
        description="A description"
    )

    new_certificate.save()

    res = Certificate.objects.filter(profile=user.profile)
    assert len(res) == 1


def test_certificates_add_fail_not_profile(create_test_user):
    """
    Test a ValidationError when Profile_ID not User
    """
    user1 = create_test_user()
    user2 = create_test_user()

    with pytest.raises(ValidationError) as e_info:
        add_certificate(
            user=user1,
            profile_id=user2.profile.id,
            title="A Title",
            description="A description",
            organization="A Organization",
            completion_date="2020-01-01")

    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info.value)
    assert ValidationError

def test_certificates_add_fail_fakefile(create_test_user):
    """
    Test a ValidationError when File is corrupted
    """

    user = create_test_user()
    fake_jpg_file = 'test/files/FAKE_JPG.jpg'

    with pytest.raises(ValidationError):
        add_certificate(
            user=user,
            profile_id=user.profile.id,
            title="A Title",
            document=fake_jpg_file,
            description="A description",
            organization="A Organization",
            completion_date="2020-01-01")

    assert ValidationError


def test_certificates_update_success(create_test_user):
    """
    Test Certificate successfully updated
    """
    user1 = create_test_user()
    certificate = mixer.blend(Certificate,
                              profile=user1.profile)

    updated_certificate = update_certificate(
        user=user1,
        profile_id=user1.profile.id,
        id=certificate.id,
        title="A updated Title",
        description="A updated description",
        organization="A updated Organization",
        completion_date="2020-01-01")

    assert Certificate.objects.get(id=certificate.id) == updated_certificate

def test_certificates_update_success_required_fields(create_test_user):
    """
    Test Certificate successfully updated with required fields
    """
    user1 = create_test_user()
    certificate = mixer.blend(Certificate,
                              profile=user1.profile)

    updated_certificate = update_certificate(
        user=user1,
        profile_id=user1.profile.id,
        id=certificate.id,
        title="A updated Title",
        description="A updated description")

    assert Certificate.objects.get(id=certificate.id) == updated_certificate
    assert updated_certificate.organization is None


def test_certificates_update_fail_not_profile(create_test_user):
    """
    Test certificates update fail not profile
    """
    user1 = create_test_user()
    user2 = create_test_user()
    certificate = mixer.blend(Certificate,
                              profile=user1.profile)

    with pytest.raises(ValidationError) as e_info:
        update_certificate(
            user=user2,
            profile_id=user1.profile.id,
            id=certificate.id,
            title="A updated Title",
            description="A updated description",
            organization="A updated Organization",
            completion_date="2020-01-01")

    with pytest.raises(ValidationError) as e_info_2:
        update_certificate(
            user=user2,
            profile_id=user2.profile.id,
            id=certificate.id,
            title="A updated Title",
            description="A updated description",
            organization="A updated Organization",
            completion_date="2020-01-01")

    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info.value)
    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info_2.value)
    assert ValidationError


def test_certificates_delete_success(create_test_user):
    """
    Test Certificate successfully deleted
    """
    user = create_test_user()

    certificate = mixer.blend(Certificate,
                              profile=user.profile)

    delete_certificate(
        user=user,
        id=certificate.id
    )

    exists = Certificate.objects.filter(
        profile=user.profile,
        id=certificate.id).exists()
    assert exists is False


def test_certificates_delete_fail_not_profile(create_test_user):
    """
    Test Certificate failed not Profile
    """
    user = create_test_user()
    user2 = create_test_user()

    certificate = mixer.blend(Certificate,
                              profile=user.profile)

    with pytest.raises(ValidationError) as e_info:
        delete_certificate(
            user=user2,
            id=certificate.id
        )
    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info.value)
    assert ValidationError
