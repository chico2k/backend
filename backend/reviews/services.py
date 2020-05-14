from reviews.models import Review, ReviewResponse
from profiles.models import Profile

from reviews.constants import Errors
from django.core.exceptions import ValidationError
from django.db.models import Avg


def add_review_to_profile(user, profile_id, title, description, rating):
    """
    Add new Review to Profile
    """
    profile = Profile.objects.get(id=profile_id)

    """
    Validation: Is Sporttype already present?
    """
    if Review.objects.filter(profile=profile_id, author=user.profile).exists():
        raise ValidationError(
            {'non_field_errors': Errors.RATING_AUTHOR_EXISITS})

    """
     Validation: Author cannot be the Owner of Profile
    """
    if user.profile == profile:
        raise ValidationError(
            {'non_field_errors': Errors.RATING_OWNER_CANNOT_AUTHOR})

    """
    Create new Review
    """
    review = Review.objects.create(
        profile=profile,
        title=title,
        description=description,
        rating=rating,
        author=user.profile
    )
    review.save()

    return review


def profile_update_rating_numbers(instance):
    """
    Update Number of Ratings and average of Ratings in Profile
    """
    profile = Profile.objects.get(id=instance.profile.id)
    review_numbers = Review.objects.filter(
        profile=instance.profile,
        is_published=True).count()
    review_average = Review.objects.filter(
        profile=instance.profile,
        is_published=True).aggregate(Avg('rating'))

    profile.number_rating = review_numbers
    profile.average_rating = round(review_average['rating__avg'], 1)

    profile.save()
    return profile


def review_response_add(
        user,
        profile_id,
        review_id,
        description):
    """
    Add Review Response to Review
    """
    review = Review.objects.get(id=review_id)

    """
    Validation: Is Response already present?
    """
    if ReviewResponse.objects.filter(review=review_id, author=user.profile).exists():
        raise ValidationError(
            {'non_field_errors': Errors.RESPONSE_AUTHOR_EXISITS})
    """
    Validation: Is Author Owner of Profile?
    """
    if user.profile != review.profile:
        raise ValidationError(
            {'non_field_errors': Errors.RESPONSE_NOT_ALLOWED})

    """
    Create new Review Response
    """
    review_response = ReviewResponse.objects.create(
        review=review,
        description=description,
        author=user.profile,
    )
    review_response.save()

    return review_response
