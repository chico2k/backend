from certificates.models import Certificate
from django.core.exceptions import ValidationError

from main.messages.messages import Errors


def add_certificate(user,
                    profile_id,
                    title,
                    description,
                    organization=None,
                    completion_date=None,
                    document=None):
    """
    Add a new Certificate to Profile
    """
    profile = user.profile

    """
    Validation: Is Profile ID in URL same as User?
    """
    if (profile_id != user.id):
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})

    certificate = Certificate.objects.create(
        profile=profile,
        title=title,
        description=description,
        organization=organization,
        document=document,
        completion_date=completion_date)
    certificate.save()

    return certificate


def update_certificate(user,
                       profile_id,
                       id,
                       title,
                       description,
                       organization=None,
                       completion_date=None,
                       document=None):
    """
    Update Experience to Profile
    """
    certificate = Certificate.objects.get(id=id)

    """
    Validation: Is Profile ID in URL same as User?
    """
    if (profile_id != user.profile.id):
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})
    """
    Validation: Is User same as Profile?
    """
    if (certificate.profile != user.profile):
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})

    """
    Database: Update Certificate
    """
    certificate.title = title
    certificate.description = description
    certificate.organization = organization
    certificate.document = document
    certificate.completion_date = completion_date
    certificate.save()

    return certificate


def delete_certificate(user, id):
    """
    Delete a Certificate from Profile
    """
    certificate = Certificate.objects.get(id=id)
    """
    Validation: Is own Profile/Sport?
    """
    if user.profile != certificate.profile:
        raise ValidationError(
            {'non_field_errors': Errors.ACTION_NOT_ALLOWED})

    certificate.delete()
    return
