from django.db import models
from django.utils.translation import ugettext_lazy as _

LEVELS = [
    (1, _('Beginner')),
    (2, _('Advanced')),
    (3, _('Expert')),
]


class Sport(models.Model):
    """
    Sports Model for the DB
    """

    profile = models.ForeignKey(
        to="profiles.Profile",
        related_name='sport',
        on_delete=models.CASCADE,
        blank=False, null=False)

    sporttype = models.ForeignKey(
        to="sports.Sporttype",
        related_name='sporttype',
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    level = models.IntegerField(
        choices=LEVELS,
        default=1,
        blank=False, null=False)

    def __str__(self):
        return (f'{self.profile} - {self.sporttype} - {self.level}')

    class Meta:
        verbose_name = _("Sport")
        verbose_name_plural = _("Sports")

        ordering = ['-level', '-sporttype']

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)


class Sporttype(models.Model):
    """
    Sporttype for the DB
    """

    title = models.CharField(max_length=255, unique=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Sporttype")
        verbose_name_plural = _("Sporttypes")

        ordering = ['-title']

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)
