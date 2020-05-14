from mixer.backend.django import mixer
from experiences.models import Experience
from django.contrib.auth import get_user_model
User = get_user_model()


def test_experience_string_correct(create_test_user):
    """
    Test Experience String
    """
    user1 = create_test_user()
    review = mixer.blend(Experience, profile=user1.profile)

    assert str(review) == f'{review.profile}: {review.title}'
