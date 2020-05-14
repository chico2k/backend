from profiles.models import Profile

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .constants import Errors


def update_profile(user, is_guide, profile_id):
    """
    Update a Sport to Profile
    """
    profile = get_object_or_404(Profile, id=profile_id)

    """
    Validation: Is own Profile/Sport?
    """
    if user.profile.id != profile.id:
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})

    """
    Database: Update Sporttype
    """
    profile.is_guide = is_guide
    profile.save()
    return profile
