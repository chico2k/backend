from experiences.models import Experience
from experiences.services import \
    add_experience, \
    update_experience, \
    delete_experience
import pytest
from django.core.exceptions import ValidationError
from main.messages.messages import Errors


def test_experiences_add_success(create_test_user):
    """
    Test Experience added to Profile
    """
    user = create_test_user()

    add_experience(
        profile_id=user.profile.id,
        user=user,
        title="A Title",
        description="A description",
        from_date="2020-01-01",
        to_date="2020-12-31",
        is_current=True)

    res = Experience.objects.filter(profile=user.profile)
    assert len(res) == 1


def test_experiences_add_fail_not_profile(create_test_user):
    """
    Test a ValidationError when Profile_ID not User
    """
    user1 = create_test_user()
    user2 = create_test_user()

    with pytest.raises(ValidationError) as e_info:
        add_experience(
            profile_id=user1.profile.id,
            user=user2,
            title="A Title",
            description="A description",
            from_date="2020-01-01",
            to_date="2019-12-31",
            is_current=True)
    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info.value)
    assert ValidationError


def test_experiences_add_fail_date(create_test_user):
    """
    Test To Date not later than From Date
    """
    user1 = create_test_user()

    with pytest.raises(ValidationError) as e_info:
        add_experience(
            profile_id=user1.profile.id,
            user=user1,
            title="A Title",
            description="A description",
            from_date="2020-12-31",
            to_date="2019-01-01",
            is_current=True)
    assert str(Errors.EXPERIENCES_TO_DATE_NOT_LATER_FROM_DATE) in str(e_info.value)
    assert ValidationError


def test_experiences_add_success_same_date(create_test_user):
    """
    Test Experience added to Profile with same Date
    """
    user = create_test_user()

    new_experience = add_experience(
        profile_id=user.profile.id,
        user=user,
        title="A Title",
        description="A description",
        from_date="2020-01-01",
        to_date="2020-01-01",
        is_current=True)

    res = Experience.objects.filter(profile=user.profile)
    assert len(res) == 1
    assert new_experience == res[0]


def test_experiences_update_success(create_test_user):
    """
    Test Experience updated to Profile
    """
    user = create_test_user()

    new_experience = add_experience(
        profile_id=user.profile.id,
        user=user,
        title="A Title",
        description="A description",
        from_date="2020-01-01",
        to_date="2020-01-01",
        is_current=True)

    updated_experience = update_experience(
        user=user,
        profile_id=user.profile.id,
        id=new_experience.id,
        title="A updated Title",
        description="A updated description",
        from_date="2019-01-01",
        to_date="2019-01-01",
        is_current=False
    )
    res = Experience.objects.filter(profile=user.profile)
    assert len(res) == 1
    assert updated_experience == res[0]


def test_experiences_update_fail_not_profile(create_test_user):
    """
    Test Experience updated to Profile fail not
    """
    user = create_test_user()
    user2 = create_test_user()

    new_experience = add_experience(
        profile_id=user.profile.id,
        user=user,
        title="A Title",
        description="A description",
        from_date="2020-01-01",
        to_date="2020-01-01",
        is_current=True)

    with pytest.raises(ValidationError) as e_info:
        update_experience(
            user=user2,
            profile_id=user.profile.id,
            id=new_experience.id,
            title="A updated Title",
            description="A updated description",
            from_date="2019-01-01",
            to_date="2019-01-01",
            is_current=False
        )
    assert str(Errors.ACTION_NOT_ALLOWED) in str(e_info.value)
    assert ValidationError


def test_experiences_delete_success(create_test_user):
    """
    Test Experience deleted successfully
    """
    user = create_test_user()

    new_experience = add_experience(
        profile_id=user.profile.id,
        user=user,
        title="A Title",
        description="A description",
        from_date="2020-01-01",
        to_date="2020-01-01",
        is_current=True)

    delete_experience(user, id=new_experience.id)

    assert len(Experience.objects.filter(profile=user.profile)) == 0


def test_experiences_delete_fail_not_profile(create_test_user):
    """
    Test Experience deleted fail because not own Profile
    """
    user = create_test_user()
    user2 = create_test_user()

    new_experience = add_experience(
        profile_id=user.profile.id,
        user=user,
        title="A Title",
        description="A description",
        from_date="2020-01-01",
        to_date="2020-01-01",
        is_current=True)

    with pytest.raises(ValidationError) as error:
        delete_experience(user2, id=new_experience.id)
    assert str(Errors.ACTION_NOT_ALLOWED) in str(error.value)
    assert ValidationError
