from mixer.backend.django import mixer
from reviews.models import Review, ReviewResponse
from django.contrib.auth import get_user_model
User = get_user_model()


def test_review_string_correct(create_test_user):
    """
    Test Review String
    """
    user1 = create_test_user()
    user2 = create_test_user()
    review = mixer.blend(Review, profile=user1.profile,
                         author=user2.profile, rating=5)

    assert str(
        review) == f'Review for Profile: {review.profile} with Rating: {review.rating}'


def test_review_added_successful(create_test_user):
    """
    Test Review added successfully
    """
    user1 = create_test_user()
    author = create_test_user()
    author2 = create_test_user()

    mixer.blend(Review, profile=user1.profile,
                author=author.profile, rating=5)
    mixer.blend(Review, profile=user1.profile,
                author=author2.profile, rating=3)

    exists = Review.objects.all()

    assert len(exists) == 2


def test_review_response_string_correct(create_test_user):
    """
    Test Review Response String
    """
    user1 = create_test_user()
    user2 = create_test_user()
    review = mixer.blend(Review, profile=user1.profile,
                         author=user2.profile, rating=5)

    review_response = mixer.blend(ReviewResponse,
                                  author=user1.profile,
                                  review=review)

    assert str(
        review_response) == f'Review Response for Review: {review_response.review.id}'


def test_review_response_is_published(create_test_user):
    """
    Test Review Response is published default
    """
    user1 = create_test_user()
    user2 = create_test_user()
    review = mixer.blend(Review, profile=user1.profile,
                         author=user2.profile, rating=5)

    review_response = ReviewResponse.objects.create(
        author=user1.profile,
        review=review,
        description="A Review Response Description"
    )
    assert review_response.is_published is True
