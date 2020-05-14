from sports.selectors import get_list_sport_of_profile, \
    get_detail_sport_of_profile,\
    get_list_sporttype_to_add
from mixer.backend.django import mixer
from sports.models import Sport, Sporttype
from rest_framework.exceptions import NotFound

from django.contrib.auth import get_user_model
User = get_user_model()


def test_list_sport_of_profile():
    """
    Test only users for valid Profile ID will be shown
    """
    user1 = mixer.blend(User)
    user2 = mixer.blend(User)
    mixer.blend(Sport, profile=user1.profile)
    mixer.blend(Sport, profile=user1.profile)
    mixer.blend(Sport, profile=user2.profile)
    result = get_list_sport_of_profile(profile=user1.profile.id)

    assert len(result) == 2


def test_list_sport_of_profile_raise404():
    """
    Test Not Found when Profile has no Sports
    """
    user1 = mixer.blend(User)
    mixer.blend(Sport, profile=user1.profile)
    try:
        get_list_sport_of_profile(profile=2)
    except NotFound:
        assert True


def test_get_detail_sport_of_profile():
    """
    Test that only Sport for specific ID is shown
    """
    user1 = mixer.blend(User)
    sport1 = mixer.blend(Sport, profile=user1.profile)
    mixer.blend(Sport, profile=user1.profile)
    result = get_detail_sport_of_profile(id=sport1.id)
    assert result == sport1


def test_get_list_sporttype_to_add():
    """
    Test that only availabel Sport for Profile are shown
    """
    user1 = mixer.blend(User)
    sporttype1 = mixer.blend(Sporttype)
    mixer.blend(Sporttype)
    mixer.blend(Sporttype)

    mixer.blend(Sport, sporttype=sporttype1, profile=user1.profile)

    result = get_list_sporttype_to_add(user1.profile)
    assert len(result) == 2
    assert sporttype1 not in result
