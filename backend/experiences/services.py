from .models import Experience
from django.core.exceptions import ValidationError

from main.messages.messages import Errors


def add_experience(
        user,
        profile_id,
        title,
        description,
        from_date,
        to_date,
        is_current):
    """
    Add a new Experience to Profile
    """
    profile = user.profile

    """
    Validation: Is Profile ID in URL same as User?
    """
    if (profile_id != user.id):
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})
    """
    Validation: To later than From Date?
    """
    if (from_date > to_date):
        raise ValidationError(
            {'non_field_errors': Errors.EXPERIENCES_TO_DATE_NOT_LATER_FROM_DATE})

    experience = Experience.objects.create(
        profile=profile,
        title=title,
        description=description,
        from_date=from_date,
        to_date=to_date,
        is_current=is_current)
    experience.save()

    return experience


def update_experience(user,
                      profile_id,
                      id,
                      title,
                      description,
                      from_date,
                      to_date,
                      is_current):
    """
    Update Experience to Profile
    """
    experience = Experience.objects.get(id=id)

    """
    Validation: Is Profile ID in URL same as User?
    """
    if (profile_id != user.profile.id):
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})
    """
    Validation: Is User same as Profile?
    """
    if (experience.profile != user.profile):
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})
    """
    Validation: To later than From Date?
    """
    if (from_date > to_date):
        raise ValidationError(
            {'non_field_errors': Errors.EXPERIENCES_TO_DATE_NOT_LATER_FROM_DATE})

    """
    Database: Update Sporttype
    """
    experience.title = title
    experience.description = description
    experience.from_date = from_date
    experience.to_date = to_date
    experience.is_current = is_current
    experience.save()

    return experience


def delete_experience(user, id):
    """
    Delete a Experience from Profile
    """
    experience = Experience.objects.get(id=id)
    """
    Validation: Is own Profile/Sport?
    """
    if user.profile != experience.profile:
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})

    experience.delete()
    return
