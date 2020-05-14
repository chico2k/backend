from reviews.selectors import get_list_reviews_of_profile
from mixer.backend.django import mixer
from reviews.models import Review
from django.contrib.auth import get_user_model
User = get_user_model()


def test_get_list_reviews_of_profile():
    """
    Test only published Reviews for Profile will be show
    """
    user1 = mixer.blend(User)
    user2 = mixer.blend(User)

    mixer.blend(Review,
                profile=user1.profile,
                rating=2,
                author=mixer.blend(User).profile),

    mixer.blend(Review,
                profile=user1.profile,
                author=mixer.blend(User).profile,
                rating=3,
                is_published=False)
    mixer.blend(Review,
                profile=user2.profile,
                rating=3.5,
                author=mixer.blend(User).profile),

    result = get_list_reviews_of_profile(profile=user1.profile.id)

    assert len(result) == 1


def test_get_list_reviews_of_profile_raise404():
    """
    Test get_list_reviews_of_profile raise 404 for not found
    """
    assert len(get_list_reviews_of_profile(profile=3)) == 0
