from profiles.constants import Errors
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile
import pytest

User = get_user_model()


"""
URLS
"""
PROFILE_URL = reverse('profiles:list')


def get_profile_detail_url(profile_id):
    """
    Return URL for Detail Profile
    """
    return reverse('profiles:detail', args=[profile_id])


def get_profile_update_url(profile_id):
    """
    Return URL for Detail Profile
    """
    return reverse('profiles:update', args=[profile_id])


"""
Test for public requests
"""


def test_profile_list_shown_to_unauthenticated_user():
    """
    Test that unauthorized Users can see Profile List
    """
    client = APIClient()
    res = client.get(PROFILE_URL)
    assert res.status_code == status.HTTP_200_OK


def test_profiles_are_shown_in_response(create_test_user):
    """
    Test that a list of users is shown
    """
    client = APIClient()
    create_test_user()
    create_test_user()
    print(client)
    res = client.get(PROFILE_URL)
    assert len(res.data['results']) == 2


def test_active_users_are_shown_only(create_test_user):
    """
    Test that only Profiles from active Users are shown
    """
    client = APIClient()
    create_test_user()
    create_test_user(is_active=False)

    res = client.get(PROFILE_URL)
    assert len(res.data['results']) == 1


def test_detail_page_available_for_unauthenticated(create_test_user):
    """
    Detail Page can be loaded for unauthenticated User
    """
    client = APIClient()
    user1 = create_test_user()
    url = get_profile_detail_url(user1.id)
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK


"""
Test for private requests
"""


def test_user_detail_page_only_one_user(create_test_user):
    """
    Test only one User Detail Page is shown
    """
    client = APIClient()
    user1 = create_test_user()
    client.force_authenticate(user=user1)
    url = get_profile_detail_url(user1.id)
    res = client.get(url)
    assert user1.id == res.data['id']


def test_put_to_user_gives_200(create_test_user):
    """
    Test that Put to User Profile is 200
    """
    client = APIClient()
    user1 = create_test_user()
    client.force_authenticate(user1)
    payload = {
        id: user1.id
    }
    url = get_profile_update_url(user1.id)
    res = client.put(url, payload)
    assert res.status_code == status.HTTP_200_OK


def test_put_works_for_own_profile(create_test_user):
    """
    Test that Put to User Profile is working for Owner
    """
    client = APIClient()
    user1 = create_test_user()
    client.force_authenticate(user1)
    payload = {
        'is_guide': True
    }
    url = get_profile_update_url(user1.id)
    res = client.put(url, payload)

    update_profile = Profile.objects.get(id=user1.profile.id)

    assert update_profile.is_guide == payload['is_guide']
    assert res.status_code == status.HTTP_200_OK


def test_put_not_working_for_other_profiles(create_test_user):
    """
    Test that Put to User Profile not working for other Profiles
    """
    client = APIClient()
    new_user = create_test_user()
    new_user2 = create_test_user()

    client.force_authenticate(new_user)
    payload = {
        'is_guide': True
    }
    url = get_profile_update_url(new_user2.id)

    with pytest.raises(Exception) as e:
        client.put(url, payload)
        assert str(Errors.ACTION_NOT_ALLOWED) in str(e.value)


def test_delete_methode_not_allowed(create_test_user):
    """
    Test that delete Methode is not allwowed
    """
    client = APIClient()
    new_user = create_test_user()
    client.force_authenticate(new_user)
    url = get_profile_detail_url(new_user.id)
    res = client.delete(url)
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_create_methode_not_allowed(create_test_user):
    """
    Test that create Methode is not allwowed
    """
    client = APIClient()
    new_user = create_test_user()
    client.force_authenticate(new_user)
    url = get_profile_detail_url(new_user.id)
    res = client.post(url, {})
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
