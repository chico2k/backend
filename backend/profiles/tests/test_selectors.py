from profiles.selectors import get_active_profiles, get_active_guides
from django.contrib.auth import get_user_model
User = get_user_model()


def test_get_active_profiles(create_test_user):
    """
    Get active Profile List shows only active users
    """
    create_test_user()
    create_test_user()
    create_test_user(is_active=False)

    exists = get_active_profiles()

    assert len(exists) == 2


def test_get_single_active_profile(create_test_user):
    """
    Test only single active profile when profile id passed
    """
    user = create_test_user()
    create_test_user()
    exists = get_active_profiles(profile_id=user.profile.id)

    assert user.profile.id == exists.id


def test_get_active_guides(create_test_user):
    """
    Test only active guides are returned
    """
    create_test_user()

    user_guide_notactive = create_test_user(is_active=False)
    user_guide_notactive.profile.is_guide = True
    user_guide_notactive.save()

    user_guide_active = create_test_user()
    user_guide_active.profile.is_guide = True
    user_guide_active.save()

    assert len(get_active_guides()) == 1
