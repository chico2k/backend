from experiences.models import Experience
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound


def get_list_experience_of_profile(*, profile):
    """
    Get all experiences for Profile Raise 404 if not found
    """
    experience = Experience.objects.filter(profile__id=profile)
    if not experience:
        raise NotFound
    return experience


def get_detail_experience_of_profile(*, id):
    """
    Get Detail Experience for a Profile
    """
    return get_object_or_404(Experience, id=id)
