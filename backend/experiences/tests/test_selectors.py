from mixer.backend.django import mixer
from experiences.models import Experience
from django.contrib.auth import get_user_model
from experiences.selectors import \
    get_list_experience_of_profile, \
    get_detail_experience_of_profile
from rest_framework.exceptions import NotFound
User = get_user_model()


def test_experiences_list_success():
    """
    Test Experiences shown for Profile ID
    """
    user1 = mixer.blend(User)
    user2 = mixer.blend(User)
    mixer.blend(Experience, profile=user1.profile)
    mixer.blend(Experience, profile=user1.profile)
    mixer.blend(Experience, profile=user2.profile)
    result = get_list_experience_of_profile(profile=user1.profile.id)

    assert len(result) == 2


def test_experiences_list_fail_404():
    """
    Test Not Found when Profile has no Experiences
    """
    user1 = mixer.blend(User)
    mixer.blend(Experience, profile=user1.profile)
    try:
        get_list_experience_of_profile(profile=2)
    except NotFound:
        assert True


def test_experiences_detail_success():
    """
    Test that only Experience for specific ID is shown
    """
    user1 = mixer.blend(User)
    sport1 = mixer.blend(Experience, profile=user1.profile)
    mixer.blend(Experience, profile=user1.profile)
    result = get_detail_experience_of_profile(id=sport1.id)
    assert result == sport1
