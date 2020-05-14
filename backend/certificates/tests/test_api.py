from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from certificates.models import Certificate
from mixer.backend.django import mixer
from main.messages.messages import Errors, Success
from certificates.api import CertificateDetailAPI, CertificateCreateAPI
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File

"""
URLS
"""
def get_certificates_list_url(profile_id):
    """
    Return URL for List Certificates
    """
    return reverse('profiles:certificates:list', args=[profile_id])


def get_certificates_detail_url(profile_id, pk):
    """
    Return URL for Detail Certificate
    """
    return reverse('profiles:certificates:detail', args=[profile_id, pk])

def get_certificates_create_url(profile_id):
    """
    Return URL for Create Certificate
    """
    return reverse('profiles:certificates:create', args=[profile_id])

def get_certificate_update_url(profile_id, pk):
    """
    Return URL for Update Certificates
    """
    return reverse('profiles:certificates:update', args=[profile_id, pk])


def get_certificate_delete_url(profile_id, pk):
    """
    Return URL for Delete Certificates
    """
    return reverse('profiles:certificates:delete', args=[profile_id, pk])


"""
Test Cases
"""

def test_certificates_list_success_shown(create_test_user):
    """
    Test List Certificates is shown to Unauthorized User
    (Unauthenticated)
    """
    user1 = create_test_user()
    mixer.blend(Certificate, profile=user1.profile)
    client = APIClient()
    url = get_certificates_list_url(user1.profile.id)
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK

def test_certificates_list_success_only_profile_certificates(create_test_user):
    """
    Test that ListView shows only Certificates of Profile
    """
    user1 = create_test_user()
    user2 = create_test_user()

    mixer.blend(Certificate, profile=user1.profile)
    mixer.blend(Certificate, profile=user1.profile)
    mixer.blend(Certificate, profile=user2.profile)

    client = APIClient()
    url = get_certificates_list_url(user1.profile.id)
    res = client.get(url)

    assert len(res.data) == 2
    assert res.status_code == status.HTTP_200_OK

def test_certificates_detail_success_only_profile(create_test_user):
    """
    Test that DetailView shows only Detail of Certificate
    (Unauthenticated)
    """
    user1 = create_test_user()
    mixer.blend(Certificate, profile=user1.profile)
    mixer.blend(Certificate, profile=user1.profile)
    certificate = mixer.blend(Certificate, profile=user1.profile)

    client = APIClient()
    url = get_certificates_detail_url(profile_id=user1.profile.id, pk=certificate.id)
    res = client.get(url)

    serializer = CertificateDetailAPI.OutputSerializer(certificate)

    assert res.status_code == status.HTTP_200_OK
    assert serializer.data == res.data


def test_certificates_add_success(create_test_user):
    """
    Test Certificates added successfully to own Profile
    """
    user1 = create_test_user()

    client = APIClient()

    url = get_certificates_create_url(profile_id=user1.profile.id)

    jpg_file = 'test/files/JPG.jpg'
    data = File(open(jpg_file, 'rb'))
    upload_file = SimpleUploadedFile('data.dump', data.read(), content_type='multipart/form-data')

    new_certificate = {
        'title': 'A title',
        'description': 'A description',
        'organization': 'A organization',
        'completion_date': '2020-12-31',
        'document': upload_file
    }

    client.force_authenticate(user1)
    res = client.post(url, new_certificate, format='multipart')

    new_certificate = Certificate.objects.get(
        profile=user1.profile)

    exists = Certificate.objects.filter(profile=user1.profile).exists()

    serializer = CertificateCreateAPI.OutputSerializer(new_certificate, many=False,)

    assert exists is True
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data == serializer.data

def test_certificates_add_fail_unauthenticated(create_test_user):
    """
    Test Certificates added failed unauthenticated
    """
    user1 = create_test_user()
    client = APIClient()
    url = get_certificates_create_url(profile_id=user1.profile.id)
    res = client.post(url)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_certificates_add_fail_not_profile(create_test_user):
    """
    Test Certificates added failed not Profile
    """
    user1 = create_test_user()
    user2 = create_test_user()

    jpg_file = 'test/files/JPG.jpg'
    data = File(open(jpg_file, 'rb'))
    upload_file = SimpleUploadedFile('data.dump', data.read(), content_type='multipart/form-data')

    new_certificate = {
        'title': 'A title',
        'description': 'A description',
        'organization': 'A organization',
        'completion_date': '2020-12-31',
        'document': upload_file
    }
    client = APIClient()
    client.force_authenticate(user1)

    url = get_certificates_create_url(profile_id=user2.profile.id)
    res = client.post(url, new_certificate)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Errors.ACTION_NOT_ALLOWED in res.data['non_field_errors']


def test_certificates_update_success(create_test_user):
    """
    Test Certificates updated successfully
    """
    user1 = create_test_user()
    new_certificate = mixer.blend(Certificate, profile=user1.profile)

    client = APIClient()
    url = get_certificate_update_url(
        profile_id=user1.profile.id,
        pk=new_certificate.id)
    client.force_authenticate(user1)

    jpg_file = 'test/files/JPG.jpg'
    data = File(open(jpg_file, 'rb'))
    upload_file = SimpleUploadedFile('data.dump', data.read(), content_type='multipart/form-data')

    new_certificate = {
        'title': 'A title',
        'description': 'A description',
        'organization': 'A organization',
        'completion_date': '2020-12-31',
        'document': upload_file
    }

    res = client.put(url, new_certificate)

    updated_certificate = Certificate.objects.get(
        profile=user1.profile)

    exists = Certificate.objects.filter(profile=user1.profile).exists()
    serializer = CertificateCreateAPI.OutputSerializer(updated_certificate, many=False,)

    assert exists is True
    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

def test_certificates_update_fail_not_profile(create_test_user):
    """
    Test Certificates updated not successfull not own profile
    """
    user1 = create_test_user()
    user2 = create_test_user()
    new_certificate = mixer.blend(Certificate, profile=user1.profile)

    client = APIClient()
    url = get_certificate_update_url(
        profile_id=user1.profile.id,
        pk=new_certificate.id)
    client.force_authenticate(user2)

    jpg_file = 'test/files/JPG.jpg'
    data = File(open(jpg_file, 'rb'))
    upload_file = SimpleUploadedFile('data.dump', data.read(), content_type='multipart/form-data')

    new_certificate = {
        'title': 'A title',
        'description': 'A description',
        'organization': 'A organization',
        'completion_date': '2020-12-31',
        'document': upload_file
    }

    res = client.put(url, new_certificate)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Errors.ACTION_NOT_ALLOWED in res.data['non_field_errors']

def test_certificates_delete_success(create_test_user):
    """
    Test Certificates deleted successfully
    """
    user1 = create_test_user()
    new_certificate = mixer.blend(Certificate, profile=user1.profile)

    client = APIClient()
    url = get_certificate_delete_url(
        profile_id=user1.profile.id,
        pk=new_certificate.id)
    client.force_authenticate(user1)

    res = client.delete(url)

    exists = Certificate.objects.filter(
        profile=user1.profile).exists()
    assert exists is False
    assert res.status_code == status.HTTP_200_OK
    assert res.data['message'] == Success.DELETED_SUCCESSFULLY

def test_certificates_delete_fail_not_profile(create_test_user):
    """
    Test Certificates deleted fail not Profile
    """
    user1 = create_test_user()
    user2 = create_test_user()
    new_certificate = mixer.blend(Certificate, profile=user1.profile)

    client = APIClient()
    url = get_certificate_delete_url(
        profile_id=user1.profile.id,
        pk=new_certificate.id)
    client.force_authenticate(user2)

    res = client.delete(url)

    exists = Certificate.objects.filter(
        profile=user1.profile).exists()

    assert exists is True
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Errors.ACTION_NOT_ALLOWED in res.data['non_field_errors']
