from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    """
    Profile Model for the DB
    """
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
    )
    is_guide = models.BooleanField(
        default=False,
        verbose_name=_("Guide"))
    number_rating = models.IntegerField(
        default=0)
    average_rating = models.DecimalField(
        default=0,
        max_digits=3,
        decimal_places=2)

    @property
    def name_indexing(self):
        return self.user.name

    @property
    def is_guide_indexing(self):
        if self.is_guide is True:
            return "Yes"
        elif self.is_guide is False:
            return "No"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

        ordering = ['-id']
