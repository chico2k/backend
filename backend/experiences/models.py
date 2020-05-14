from django.db import models
from django.utils.translation import ugettext_lazy as _


class Experience(models.Model):
    """
    Experience Model for DB
    """
    profile = models.ForeignKey(
        to="profiles.Profile",
        related_name='experience_profile',
        on_delete=models.CASCADE, blank=False, null=False
    )

    title = models.CharField(
        max_length=120,
        blank=False,
        null=False)

    description = models.CharField(
        max_length=5000,
        blank=False,
        null=False)

    from_date = models.DateField(
        blank=False,
        null=False)

    to_date = models.DateField(
        blank=False,
        null=False)

    is_published = models.BooleanField(
        default=True,
        blank=False,
        null=False)

    is_current = models.BooleanField(
        default=False,
        blank=False,
        null=False)

    created_date = models.DateTimeField(
        auto_now_add=True)

    modified_date = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return f'{self.profile}: {self.title}'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Experience")
        verbose_name_plural = _("Experiences")

        ordering = ['-from_date']
