from mixer.backend.django import mixer
from sports.models import Sport, Sporttype
from django.contrib.auth import get_user_model
User = get_user_model()


def test_sporttype_string():
    """
    Test Sporttype string
    """
    sporttype = mixer.blend(Sporttype)
    assert str(sporttype) == f'{sporttype.title}'


def test_sport_types_added():
    """
    Test Sporttype can be added to DB
    """
    mixer.blend(Sporttype)
    mixer.blend(Sporttype)
    assert len(Sporttype.objects.all()) == 2


def test_sport_types_added_is_published():
    """
    Test Sporttype is not published by default
    """
    sporttype = mixer.blend(Sporttype)
    assert sporttype.is_published is False


def test_sport_can_be_added(create_test_user):
    """
    Test Sport can be added for Profile
    """
    sporttype = mixer.blend(Sporttype)
    user = create_test_user()
    Sport.objects.create(
        profile=user.profile, sporttype=sporttype, level=3)

    assert len(Sporttype.objects.all()) == 1
    assert len(User.objects.all()) == 1
    assert len(Sport.objects.all()) == 1


def test_sport_string(create_test_user):
    """
    Test Sport string
    """
    sporttype = mixer.blend(Sporttype)
    user = create_test_user()
    sport = Sport.objects.create(
        profile=user.profile, sporttype=sporttype, level=3)
    assert str(sport) == f'{sport.profile} - {sport.sporttype} - {sport.level}'
