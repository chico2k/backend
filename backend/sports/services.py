from .models import Sport
from django.core.exceptions import ValidationError

from .constants import Errors


def add_sports_of_profile(*, sporttype, level, user, profile_id):
    """
    Add a new Sport to Profile
    """
    profile = user.profile
    Sport.objects.filter(
        profile=profile)

    """
    Validation: Is Profile ID in URL same as User?
    """
    if (profile_id != user.id):
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})

    """
    Validation: Is Sporttype already present?
    """
    if Sport.objects.filter(sporttype=sporttype, profile=profile).exists():
        raise ValidationError(
            {'non_field_errors': Errors.SPORT_ALREADY_EXISTS})

    """
    Database: Create new Sporttype
    """

    sport = Sport.objects.create(
        profile=profile,
        sporttype=sporttype,
        level=level)
    sport.save()

    return sport


def update_sports_of_profile(user, level, id):
    """
    Update a Sport to Profile
    """
    sport = Sport.objects.get(id=id)

    """
    Validation: Is own Profile/Sport?
    """
    if user.profile != sport.profile:
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})

    """
    Database: Update Sporttype
    """
    sport.level = level
    sport.save()
    return sport


def delete_sports_of_profile(user, id):
    """
    Delete a Sport from Profile
    """
    sport = Sport.objects.get(id=id)
    """
    Validation: Is own Profile/Sport?
    """
    if user.profile != sport.profile:
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})

    sport.delete()
    return
