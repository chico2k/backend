from django.db import models
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    """
    Location Model for the DB
    """

    profile = models.OneToOneField(
        to="profiles.Profile",
        related_name='location',
        on_delete=models.CASCADE,
        blank=False, null=False)

    location_id = models.CharField(max_length=255, unique=True)

    place_name = models.CharField(max_length=255, unique=True)

    text = models.CharField(max_length=255, unique=True)

    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    @property
    def location_field_indexing(self):
        return {
            'lat': self.latitude,
            'lon': self.longitude,
        }

    def __str__(self):
        return (f'{self.profile}')

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

        ordering = ['-id', ]

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)
