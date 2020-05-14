from django.db import models
from django.utils.translation import ugettext_lazy as _
from main.management.validators.filevalidator import FileValidator
from main.management.validators.pathandname import PathAndRename

validate_file = FileValidator(max_size=1024 * 2000,
                              content_types=('image/jpeg', 'image/jpg',))

class Certificate(models.Model):
    """
    Certificate Model for DB
    """
    profile = models.ForeignKey(
        to="profiles.Profile",
        related_name='certificate_profile',
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

    organization = models.CharField(
        max_length=120,
        blank=True,
        null=True)

    document = models.FileField(
        validators=[validate_file],
        upload_to=PathAndRename(sub_path='certificates'),
        blank=True,
        default='')

    completion_date = models.DateField(
        blank=True,
        null=True)

    is_published = models.BooleanField(
        default=True,
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
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")

        ordering = ['-completion_date']
