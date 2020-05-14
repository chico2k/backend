from sports.models import Sport, Sporttype
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


def get_list_sport_of_profile(*, profile):
    """
    Get all sports for  Profile Raise 404 if not found
    """
    sport = Sport.objects.filter(profile_id=profile).order_by('-level')
    if not sport:
        raise NotFound
    return sport


def get_detail_sport_of_profile(*, id):
    """
    Get Detail Sport for a Profile
    """
    return get_object_or_404(Sport, id=id)


def get_list_sporttype_to_add(profile):
    """
    Get all available sports for Profile to add
    """
    sport = Sport.objects.filter(profile_id=profile).values_list('sporttype', flat=True)
    sporttype = Sporttype.objects.exclude(id__in=sport)
    return sporttype
