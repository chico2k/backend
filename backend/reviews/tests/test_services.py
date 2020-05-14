import pytest
from reviews.services import add_review_to_profile, review_response_add
from reviews.constants import Errors
from reviews.models import Review, ReviewResponse
from django.core.exceptions import ValidationError


def test_review_add_fail_author_exists(create_test_user):
    """
    Test review cannot be added - Author rated already
    """
    user = create_test_user()
    user2 = create_test_user()

    add_review_to_profile(
        user=user,
        profile_id=user2.profile.id,
        title="A Title",
        description=" A Description",
        rating=3
    )

    with pytest.raises(Exception) as e:
        add_review_to_profile(user=user,
                              profile_id=user2.profile.id,
                              title="A Title",
                              description=" A Description",
                              rating=3)
    assert str(Errors.RATING_AUTHOR_EXISITS) in str(e.value)


def test_review_add_fail_not_a_choice(create_test_user):
    """
    Test review cannot be added - Author rated already
    """
    user = create_test_user()
    user2 = create_test_user()

    with pytest.raises(Exception) as e:
        add_review_to_profile(user=user,
                              profile_id=user2.profile.id,
                              title="A Title",
                              description=" A Description",
                              rating=8)
    assert str("Value Decimal('8') is not a valid choice.") in str(e.value)


def test_review_add_success_integer(create_test_user):
    """
    Test review cannot be added - Author rated already
    """
    user = create_test_user()
    user2 = create_test_user()
    add_review_to_profile(user=user,
                          profile_id=user2.profile.id,
                          title="A Title",
                          description=" A Description",
                          rating=3.5)

    exists = Review.objects.filter(profile=user2.profile)
    assert len(exists) == 1


def test_review_add_fail_author_self_profile(create_test_user):
    """
    Test review cannot be added - Author is Profile Owner
    """
    user = create_test_user()

    with pytest.raises(Exception) as e:
        add_review_to_profile(user=user,
                              profile_id=user.profile.id,
                              title="A Title",
                              description=" A Description",
                              rating=3)
    assert str(Errors.RATING_OWNER_CANNOT_AUTHOR) in str(e.value)


def test_review_add_success(create_test_user):
    """
    Test Add Review successful
    """
    user = create_test_user()
    user2 = create_test_user()

    add_review_to_profile(
        user=user,
        profile_id=user2.profile.id,
        title="A Title",
        description=" A Description",
        rating=3
    )

    exists = Review.objects.filter(profile=user2.profile)

    assert len(exists) == 1


def test_add_reviewresponse_success(create_test_user):
    """
    Test Response can be added to Review
    """
    user = create_test_user()
    user2 = create_test_user()

    review = add_review_to_profile(
        user=user,
        profile_id=user2.profile.id,
        title="A Title",
        description=" A Description",
        rating=3
    )

    review_response_add(
        user=user2,
        profile_id=user2.profile.id,
        review_id=review.id,
        description=" A Response Description",
    )

    exists = ReviewResponse.objects.filter(review=review)

    assert len(exists) == 1


def test_reviewresponse_add_fail_twice(create_test_user):
    """
    Test Response cannot be added twice
    """
    user = create_test_user()
    user2 = create_test_user()

    review = add_review_to_profile(
        user=user,
        profile_id=user2.profile.id,
        title="A Title",
        description=" A Description",
        rating=3
    )

    review_response_add(
        user=user2,
        profile_id=user2.profile.id,
        review_id=review.id,
        description=" A Response Description",
    )

    with pytest.raises(ValidationError) as e:
        review_response_add(
            user=user2,
            profile_id=user2.profile.id,
            review_id=review.id,
            description=" A Response Description",
        )
    assert str(Errors.RESPONSE_AUTHOR_EXISITS) in str(e.value)
    assert ValidationError


def test_reviewresponse_add_not_profile(create_test_user):
    """
    Test ReviewRespone can not be added for other Profiles
    """
    user = create_test_user()
    user2 = create_test_user()
    user3 = create_test_user()

    review = add_review_to_profile(
        user=user,
        profile_id=user2.profile.id,
        title="A Title",
        description=" A Description",
        rating=3
    )

    with pytest.raises(ValidationError) as e:
        review_response_add(
            user=user3,
            profile_id=user2.profile.id,
            review_id=review.id,
            description=" A Response Description",
        )
    assert str(Errors.RESPONSE_NOT_ALLOWED) in str(e.value)
    assert ValidationError
