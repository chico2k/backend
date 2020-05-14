from profiles.services import update_profile
from profiles.constants import Errors
from profiles.models import Profile
import pytest


def test_update_profile_success(create_test_user):
    """
    Test update Profile
    """
    user = create_test_user()
    update_profile(user, is_guide=True, profile_id=user.profile.id)
    exists = Profile.objects.get(id=user.profile.id)

    assert exists.is_guide is True


def test_update_profile_fail(create_test_user):
    """
    Test update Profile fail when not own Profile
    """
    user = create_test_user()
    user2 = create_test_user()

    with pytest.raises(Exception) as e:
        update_profile(user, is_guide=True, profile_id=user2.profile.id)
        assert str(Errors.ACTION_NOT_ALLOWED) in str(e.value)
