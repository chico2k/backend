from .models import Review


def get_list_reviews_of_profile(*, profile):
    """
    Get all Reviews for Profile or Raise 404 if not found
    param: Published only
    """
    review = Review.objects.filter(profile=profile, is_published=True)
    return review
