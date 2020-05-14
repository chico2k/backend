from .models import Location


def add_location_of_profile(*,
                            location_id,
                            place_name,
                            text,
                            longitude,
                            latitude,
                            user):
    """
    Add a new Location to Profile
    """
    profile = user.profile

    """
    Database: Delete existing object
    """
    Location.objects.filter(profile=profile).delete()

    """
    Database: Create new Sporttype
    """

    location = Location.objects.create(
        location_id=location_id,
        place_name=place_name,
        longitude=longitude,
        text=text,
        latitude=latitude,
        profile=profile)
    location.save()

    return location
