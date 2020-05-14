from sports.api import SportDetailApi
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from sports.services import add_sports_of_profile

from mixer.backend.django import mixer
from sports.models import Sport, Sporttype
from django.contrib.auth import get_user_model
User = get_user_model()


"""
URLS
"""


def get_sport_list_url(profile_id):
    """
    Return List for Sport
    """
    return reverse('profiles:sports:list', args=[profile_id])


def get_sport_detail_url(profile_id, pk):
    """
    Return URL for Detail Sport
    """
    return reverse('profiles:sports:detail', args=[profile_id, pk])


def get_sport_create_url(profile_id):
    """
    Return URL for Create Sport
    """
    return reverse('profiles:sports:create', args=[profile_id])


def get_sport_update_url(profile_id, pk):
    """
    Return URL for Update Sport
    """
    return reverse('profiles:sports:update', args=[profile_id, pk])


def get_sport_delete_url(profile_id, pk):
    """
    Return URL for Delete Sport
    """
    return reverse('profiles:sports:delete', args=[profile_id, pk])


"""
Test Cases
"""


def test_sport_list_shown_to_unauthenticated_usercreate_test_user(create_test_user):
    """
    Test that unauthorized Users can see Sport List (Unauthenticated)
    """
    user1 = create_test_user()
    mixer.blend(Sport, profile=user1.profile)
    client = APIClient()
    url = get_sport_list_url(user1.profile.id)
    res = client.get(url)
    assert res.status_code == status.HTTP_200_OK


def test_sports_list_shows_only_one_user_sport(create_test_user):
    """
    Test that ListView shows only Sports for Profile (Unauthenticated)
    """
    user1 = create_test_user()
    user2 = create_test_user()
    add_sports_of_profile(
        user=user1,
        sporttype=mixer.blend(Sporttype),
        level=2,
        profile_id=user1.profile.id
    )
    add_sports_of_profile(
        user=user1,
        sporttype=mixer.blend(Sporttype),
        level=2,
        profile_id=user1.profile.id
    )
    add_sports_of_profile(
        user=user2,
        sporttype=mixer.blend(Sporttype),
        level=2,
        profile_id=user2.profile.id
    )
    client = APIClient()
    url = get_sport_list_url(user1.profile.id)
    res = client.get(url)

    assert len(res.data) == 2
    assert res.status_code == status.HTTP_200_OK


def test_sport_detail_shows_one_entry(create_test_user):
    """
    Test that DetailView shows only Detail of Sport (Unauthenticated)
    """
    user1 = create_test_user()
    sport = add_sports_of_profile(
        user=user1,
        sporttype=mixer.blend(Sporttype),
        level=2,
        profile_id=user1.profile.id
    )
    client = APIClient()
    url = get_sport_detail_url(profile_id=user1.profile.id, pk=sport.id)
    res = client.get(url)

    serializer = SportDetailApi.OutputSerializer(sport)

    assert res.status_code == status.HTTP_200_OK
    assert serializer.data == res.data


def test_sport_added_successful(create_test_user):
    """
    Test Sport can be added to own Profile (Authenticated)
    """
    user1 = create_test_user()
    sporttype = mixer.blend(Sporttype)

    new_sport = {
        'user': user1,
        'sporttype': sporttype.id,
        'level': 2,
        'profile_id': user1.profile.id
    }

    url = get_sport_create_url(profile_id=user1.profile.id)

    client = APIClient()
    client.force_authenticate(user1)
    res = client.post(url, new_sport)

    exists = Sport.objects.filter(
        profile=user1.profile, sporttype=sporttype).exists()
    assert exists is True
    assert res.status_code == status.HTTP_201_CREATED


def test_sport_updated_successful(create_test_user):
    """
    Test that a Sport is updated successful
    """
    user1 = create_test_user()
    mixer.blend(Sporttype)
    sport = add_sports_of_profile(
        user=user1,
        sporttype=mixer.blend(Sporttype),
        level=2,
        profile_id=user1.profile.id
    )

    url = get_sport_update_url(profile_id=user1.profile.id, pk=sport.id)
    client = APIClient()
    client.force_authenticate(user1)

    update_sport = {
        'level': 3
    }

    res = client.put(url, update_sport)
    updated_obj = Sport.objects.get(
        profile=user1.profile, sporttype=sport.sporttype)

    assert updated_obj.level == update_sport['level']
    assert res.status_code == status.HTTP_200_OK


def test_sport_deleted_successfull(create_test_user):
    """
    Test Sport can be deleted
    """
    user1 = create_test_user()
    sporttype = mixer.blend(Sporttype)
    sport = add_sports_of_profile(
        user=user1,
        sporttype=mixer.blend(Sporttype),
        level=2,
        profile_id=user1.profile.id
    )

    url = get_sport_delete_url(profile_id=user1.profile.id, pk=sport.id)
    client = APIClient()
    client.force_authenticate(user1)

    res = client.delete(url)

    exists = Sport.objects.filter(
        profile=user1.profile, sporttype=sporttype).exists()

    assert exists is False
    assert res.status_code == status.HTTP_200_OK
