from django.core.exceptions import ValidationError
import pytest
from sports.constants import Errors
from sports.services import add_sports_of_profile,\
    delete_sports_of_profile,\
    update_sports_of_profile
from mixer.backend.django import mixer
from sports.models import Sport, Sporttype

from django.contrib.auth import get_user_model
User = get_user_model()


def test_add_sports_of_profile_success(create_test_user):
    """
    Test that a sport is added to a Profile
    """
    user = create_test_user()
    sporttype = mixer.blend(Sporttype)

    add_sports_of_profile(
        user=user,
        sporttype=sporttype,
        level=2,
        profile_id=user.profile.id
    )
    res = Sport.objects.filter(profile=user.profile.id)
    assert len(res) == 1


def test_add_sports_of_profile_fail_already_exists(create_test_user):
    """
    Test that a ValidationError when Sport present at Profile
    """
    user = create_test_user()
    sporttype = mixer.blend(Sporttype)

    add_sports_of_profile(
        user=user,
        sporttype=sporttype,
        level=2,
        profile_id=user.profile.id
    )

    with pytest.raises(ValidationError) as e_info:
        add_sports_of_profile(
            user=user,
            sporttype=sporttype,
            level=3,
            profile_id=user.profile.id
        )
    assert str(Errors.SPORT_ALREADY_EXISTS) in str(e_info.value)
    assert ValidationError


def test_add_sports_of_profile_success_for_second_profile(create_test_user):
    """
    Test that a Sporttype can be added to more than one profile
    """

    user1 = create_test_user()
    user2 = create_test_user()
    sporttype = mixer.blend(Sporttype)

    add_sports_of_profile(
        user=user1,
        sporttype=sporttype,
        level=2,
        profile_id=user1.profile.id
    )

    add_sports_of_profile(
        user=user2,
        sporttype=sporttype,
        level=2,
        profile_id=user2.profile.id
    )

    sporttype = Sporttype.objects.all()
    res = Sport.objects.all()
    assert len(sporttype) == 1
    assert len(res) == 2


def test_add_sports_of_profile_fail_not_user(create_test_user):
    """
    Test a ValidationError when Profile_ID not User
    """
    user1 = create_test_user()
    user2 = create_test_user()
    sporttype = mixer.blend(Sporttype)

    with pytest.raises(ValidationError) as e_info:
        add_sports_of_profile(
            user=user1,
            sporttype=sporttype,
            level=2,
            profile_id=user2.profile.id
        )
    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info.value)
    assert ValidationError

def test_update_sports_of_profile_success(create_test_user):
    """
    Test that a sport is updated to a Profile
    """
    user = create_test_user()
    sporttype = mixer.blend(Sporttype)
    sport = mixer.blend(Sport, sporttype=sporttype, profile=user.profile, level=3)

    update_sports_of_profile(
        user=user,
        id=sport.id,
        level=2,

    )
    res = Sport.objects.get(profile=user.profile.id)
    assert res.level == 2


def test_update_sports_of_profile_fail_not_profile(create_test_user):
    """
    Test that a sport is not updated - not own Profile
    """
    user = create_test_user()
    user2 = create_test_user()
    sporttype = mixer.blend(Sporttype)
    sport = mixer.blend(Sport, sporttype=sporttype, profile=user.profile, level=3)

    with pytest.raises(ValidationError) as e_info:
        update_sports_of_profile(
            user=user2,
            id=sport.id,
            level=2,
        )
    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info.value)
    assert ValidationError

def test_delete_sports_of_profile_success(create_test_user):
    """
    Test that a sport is deleted to a Profile
    """
    user = create_test_user()
    sporttype = mixer.blend(Sporttype)
    sport = mixer.blend(Sport, sporttype=sporttype, profile=user.profile, level=3)

    delete_sports_of_profile(
        user=user,
        id=sport.id,
    )
    exists = Sport.objects.filter(profile=user.profile.id).exists()
    assert exists is False

def test_delete_sports_of_profile_fail_not_profile(create_test_user):
    """
    Test that a sport is not deleted to a Profile - not own Profile
    """
    user = create_test_user()
    user1 = create_test_user()
    sporttype = mixer.blend(Sporttype)
    sport = mixer.blend(Sport, sporttype=sporttype, profile=user.profile, level=3)

    with pytest.raises(ValidationError) as e_info:
        delete_sports_of_profile(
            user=user1,
            id=sport.id,
        )
    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info.value)
    exists = Sport.objects.filter(profile=user.profile.id).exists()
    assert exists is True
