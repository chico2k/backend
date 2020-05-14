from .models import Profile
from django.shortcuts import get_object_or_404


def get_active_profiles(*args, **kwargs):
    """
    Get active Profiles for List or Detail View
    """
    profile = Profile.objects.filter(
        user__is_active=True)
    if kwargs.get('profile_id'):
        profile = get_object_or_404(profile,
                                    id=kwargs.get('profile_id'))

    return profile


def get_active_guides():
    """
    Get active Guides
    """
    return get_active_profiles().filter(is_guide=True)
