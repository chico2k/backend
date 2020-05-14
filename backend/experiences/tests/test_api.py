from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from experiences.api import ExperienceDetailApi
from experiences.models import Experience
from mixer.backend.django import mixer
from main.messages.messages import Errors, Success


"""
URLS
"""
def get_experience_list_url(profile_id):
    """
    Return URL for List Experiences
    """
    return reverse('profiles:experiences:list', args=[profile_id])


def get_experience_detail_url(profile_id, pk):
    """
    Return URL for Detail Experiences
    """
    return reverse('profiles:experiences:detail', args=[profile_id, pk])


def get_experience_create_url(profile_id):
    """
    Return URL for Create Experiences
    """
    return reverse('profiles:experiences:create', args=[profile_id])


def get_experience_update_url(profile_id, pk):
    """
    Return URL for Update Experiences
    """
    return reverse('profiles:experiences:update', args=[profile_id, pk])


def get_experience_delete_url(profile_id, pk):
    """
    Return URL for Delete Experiences
    """
    return reverse('profiles:experiences:delete', args=[profile_id, pk])


"""
Test Cases
"""


def test_experiences_list_success_shown(create_test_user):
    """
    Test List Experiences is shown to Unauthorized User
    (Unauthenticated)
    """
    user1 = create_test_user()
    mixer.blend(Experience, profile=user1.profile)
    client = APIClient()
    url = get_experience_list_url(user1.profile.id)
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK


def test_experiences_list_success_only_profile_experiences(create_test_user):
    """
    Test that ListView shows only Sports for Profile
    (Unauthenticated)
    """
    user1 = create_test_user()
    user2 = create_test_user()

    mixer.blend(Experience, profile=user1.profile)
    mixer.blend(Experience, profile=user1.profile)
    mixer.blend(Experience, profile=user2.profile)

    client = APIClient()
    url = get_experience_list_url(user1.profile.id)
    res = client.get(url)

    assert len(res.data) == 2
    assert res.status_code == status.HTTP_200_OK


def test_experiences_detail_success_only_profile(create_test_user):
    """
    Test that DetailView shows only Detail of Experience
    (Unauthenticated)
    """
    user1 = create_test_user()
    mixer.blend(Experience, profile=user1.profile)
    mixer.blend(Experience, profile=user1.profile)
    experience = mixer.blend(Experience, profile=user1.profile)

    client = APIClient()
    url = get_experience_detail_url(profile_id=user1.profile.id, pk=experience.id)
    res = client.get(url)

    serializer = ExperienceDetailApi.OutputSerializer(experience)

    assert res.status_code == status.HTTP_200_OK
    assert serializer.data == res.data


def test_experiences_add_success(create_test_user):
    """
    Test Experiences added successfully to own Profile
    """
    user1 = create_test_user()

    client = APIClient()

    url = get_experience_create_url(profile_id=user1.profile.id)
    new_experience = {
        'title': 'A title',
        'description': 'A description',
        'from_date': "2020-01-01",
        'to_date': '2020-12-31'
    }

    client.force_authenticate(user1)
    res = client.post(url, new_experience)

    exists = Experience.objects.filter(
        profile=user1.profile).exists()
    assert exists is True
    assert res.status_code == status.HTTP_201_CREATED
    assert res.data['id']


def test_experiences_add_fail_unauthenticated(create_test_user):
    """
    Test Experiences added failed unauthenticated
    """
    user1 = create_test_user()
    client = APIClient()
    url = get_experience_create_url(profile_id=user1.profile.id)
    res = client.post(url)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_experiences_add_fail_not_profile(create_test_user):
    """
    Test Experiences added failed not Profile
    """
    user1 = create_test_user()
    user2 = create_test_user()

    new_experience = {
        'title': 'A title',
        'description': 'A description',
        'from_date': "2020-01-01",
        'to_date': '2020-12-31'
    }

    client = APIClient()
    client.force_authenticate(user1)

    url = get_experience_create_url(profile_id=user2.profile.id)
    res = client.post(url, new_experience)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Errors.ACTION_NOT_ALLOWED in res.data['non_field_errors']


def test_experiences_update_success(create_test_user):
    """
    Test Experiences updated successfully
    """
    user1 = create_test_user()
    new_experience = mixer.blend(Experience, profile=user1.profile)

    client = APIClient()
    url = get_experience_update_url(
        profile_id=user1.profile.id,
        pk=new_experience.id)
    client.force_authenticate(user1)

    update_experience = {
        'title': 'A updated title',
        'description': 'A updated description',
        'from_date': "2020-01-01",
        'to_date': '2020-12-31'
    }

    res = client.put(url, update_experience)

    exists = Experience.objects.filter(
        profile=user1.profile).exists()
    assert exists is True
    assert res.status_code == status.HTTP_200_OK
    assert res.data['message'] == Success.UPDATED_SUCCESSFULLY


def test_experiences_update_fail_not_profile(create_test_user):
    """
    Test Experiences update failed not Profile
    """
    user1 = create_test_user()
    user2 = create_test_user()

    new_experience = mixer.blend(Experience, profile=user1.profile)

    update_experience = {
        'title': 'A title',
        'description': 'A description',
        'from_date': "2020-01-01",
        'to_date': '2020-12-31'
    }

    client = APIClient()
    client.force_authenticate(user2)

    url = get_experience_update_url(
        profile_id=user1.profile.id,
        pk=new_experience.id)

    res = client.put(url, update_experience)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Errors.ACTION_NOT_ALLOWED in res.data['non_field_errors']


def test_experiences_delete_success(create_test_user):
    """
    Test Experiences deleted successfully
    """
    user1 = create_test_user()
    new_experience = mixer.blend(Experience, profile=user1.profile)

    client = APIClient()
    url = get_experience_delete_url(
        profile_id=user1.profile.id,
        pk=new_experience.id)
    client.force_authenticate(user1)

    res = client.delete(url)

    exists = Experience.objects.filter(
        profile=user1.profile).exists()
    assert exists is False
    assert res.status_code == status.HTTP_200_OK
    assert res.data['message'] == Success.DELETED_SUCCESSFULLY


def test_experiences_delete_fail_not_profile(create_test_user):
    """
    Test Experiences deleted fail not Profile
    """
    user1 = create_test_user()
    user2 = create_test_user()
    new_experience = mixer.blend(Experience, profile=user1.profile)

    client = APIClient()
    url = get_experience_delete_url(
        profile_id=user1.profile.id,
        pk=new_experience.id)
    client.force_authenticate(user2)

    res = client.delete(url)

    exists = Experience.objects.filter(
        profile=user1.profile).exists()

    assert exists is True
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert Errors.ACTION_NOT_ALLOWED in res.data['non_field_errors']
