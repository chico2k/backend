import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from reviews.models import Review, ReviewResponse
from reviews.constants import Errors


"""
URLS
"""


def get_review_list_url(profile_id):
    """
    Return List URL for Review
    """
    return reverse('profiles:reviews:list', args=[profile_id])


def get_review_create_url(profile_id):
    """
    Return Create URL for Review
    """
    return reverse('profiles:reviews:create', args=[profile_id])


def get_review_response_create_url(profile_id, review_id):
    """
    Return Create URL for Review Response
    """
    return reverse('profiles:reviews:create-response', args=[profile_id, review_id])


"""
Test Cases
"""


def test_list_review_not_allowed_for_unauthenticated(create_test_user):
    """
    Test that unauthorized Users cannot see Reviews (Unauthenticated)
    """
    user1 = create_test_user()
    client = APIClient()
    url = get_review_list_url(user1.profile.id)
    res = client.get(url)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_review_shown_for_authenticated(create_test_user):
    """
    Test authenticated Users can see Reviews of Profile
    """
    user1 = create_test_user()
    user2 = create_test_user()

    mixer.blend(Review,
                profile=user2.profile,
                rating=2.5,
                author=create_test_user().profile
                )

    mixer.blend(Review,
                profile=user2.profile,
                rating=2.5,
                author=create_test_user().profile
                )

    client = APIClient()
    client.force_authenticate(user1)
    url = get_review_list_url(user2.profile.id)
    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK


def test_list_review_shown_no_data_for_empty_resp(create_test_user):
    """
    Test Status Ok and Empty Response for Users with no Reviews
    """
    user1 = create_test_user()

    client = APIClient()
    client.force_authenticate(user1)

    url = get_review_list_url(user1.profile.id)
    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == []


def test_create_review_not_allowed_for_unauthenticated(create_test_user):
    """
    Test that unauthorized Users cannot create Reviews (Unauthenticated)
    """
    user1 = create_test_user()
    client = APIClient()
    url = get_review_list_url(user1.profile.id)
    res = client.post(url)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_review_allowed_for_authenticated(create_test_user):
    """
    Test authenticated Users can create Reviews (Authenticated)
    """
    user1 = create_test_user()

    user2 = create_test_user()
    url = get_review_create_url(user2.profile.id)

    review = {
        'title': 'A Title',
        'description': ' A description',
        'rating': 3
    }

    client = APIClient()
    client.force_authenticate(user1)
    res = client.post(url, review)
    exists = Review.objects.get(id=res.data['id'])

    assert res.status_code == status.HTTP_201_CREATED
    assert exists


def test_create_review_again_fails(create_test_user):
    """
    Test authenticated Users can create Reviews (Authenticated)
    """
    user1 = create_test_user()
    user2 = create_test_user()

    url = get_review_create_url(user2.profile.id)
    review1 = {
        'title': 'A Title',
        'description': ' A description',
        'rating': 3
    }
    client = APIClient()
    client.force_authenticate(user1)
    client.post(url, review1)

    review2 = {
        'title': 'A Title',
        'description': ' A description',
        'rating': 3
    }

    with pytest.raises(Exception) as e:
        client.post(url, review2)
        assert str(Errors.RATING_AUTHOR_EXISITS) in str(e.value)


def test_review_response_fail_unauthenticate(create_test_user):
    """
    Test  unauthorized Users cannot create Review Response (Unauthenticated)
    """
    user1 = create_test_user()
    user2 = create_test_user()
    review = mixer.blend(Review,
                         rating=2.5,
                         profile=user2.profile,
                         author=user1.profile)

    client = APIClient()
    url = get_review_response_create_url(user1.profile.id, review.id)
    res = client.post(url)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_review_response_success(create_test_user):
    """
    Test Review Response added
    """
    user1 = create_test_user()
    user2 = create_test_user()
    review = mixer.blend(Review,
                         rating=3.5,
                         profile=user2.profile,
                         author=user1.profile)

    client = APIClient()
    client.force_authenticate(user2)

    response = {
        'description': 'A Response Description'
    }

    url = get_review_response_create_url(user2.profile.id, review.id)
    res = client.post(url, response)

    assert res.status_code == status.HTTP_201_CREATED
    assert ReviewResponse.objects.get(id=res.data['id'])


def test_review_response_fail_delete(create_test_user):
    """
    Test Review Response cannot be deleted
    """
    user1 = create_test_user()
    user2 = create_test_user()
    review = mixer.blend(Review,
                         rating=2.5,
                         profile=user2.profile,
                         author=user1.profile)

    client = APIClient()
    client.force_authenticate(user2)
    url = get_review_response_create_url(user2.profile.id, review.id)

    res = client.delete(url)

    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_review_response_fail_update_put(create_test_user):
    """
    Test Review Response cannot be updated (Put)
    """
    user1 = create_test_user()
    user2 = create_test_user()
    review = mixer.blend(Review,
                         rating=2.5,
                         profile=user2.profile,
                         author=user1.profile)

    client = APIClient()
    client.force_authenticate(user2)
    url = get_review_response_create_url(user2.profile.id, review.id)

    res = client.put(url)

    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_review_response_fail_update_patch(create_test_user):
    """
    Test Review Response cannot be updated (Patch)
    """
    user1 = create_test_user()
    user2 = create_test_user()
    review = mixer.blend(Review,
                         rating=3.5,
                         profile=user2.profile,
                         author=user1.profile)

    client = APIClient()
    client.force_authenticate(user2)
    url = get_review_response_create_url(user2.profile.id, review.id)

    res = client.patch(url)

    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
