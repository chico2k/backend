from django.utils.translation import ugettext_lazy as _
from django.db import models

RATING_CHOICES = (
    (1.0, '1.0'),
    (1.5, '1.5'),
    (2.0, '2.0'),
    (2.5, '2.5'),
    (3.0, '3.0'),
    (3.5, '3.5'),
    (4.0, '4.0'),
    (4.5, '4.5'),
    (5.0, '5.0'),
)


class Review(models.Model):
    """
    Review Model for the DB
    """

    profile = models.ForeignKey(
        to="profiles.Profile",
        related_name='review',
        on_delete=models.CASCADE,
        blank=False, null=False)

    title = models.CharField(
        max_length=120,
        blank=False,
        null=False)

    description = models.CharField(
        max_length=5000,
        blank=False,
        null=False)

    rating = models.DecimalField(
        blank=False,
        null=False,
        max_digits=2,
        decimal_places=1,
        choices=RATING_CHOICES
        # ,
        # validators=[
        #     MinValueValidator(Decimal(1.0)),
        #     MaxValueValidator(Decimal(5.0)),]
    )

    author = models.ForeignKey(
        to="profiles.Profile",
        related_name='review_author',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    is_published = models.BooleanField(
        default=True,
        blank=False,
        null=False)

    created_date = models.DateTimeField(
        auto_now_add=True)

    modified_date = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return f'Review for Profile: {self.profile} with Rating: {self.rating}'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

        ordering = ['-created_date']


class ReviewResponse(models.Model):
    """
    Review Response Model for the DB
    """

    review = models.ForeignKey(
        to="reviews.Review",
        related_name='review',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    author = models.ForeignKey(
        to="profiles.Profile",
        related_name='review_response_author',
        on_delete=models.CASCADE,
        blank=False, null=False
    )

    description = models.CharField(
        max_length=5000,
        blank=False,
        null=False)

    is_published = models.BooleanField(
        default=True,
        blank=False,
        null=False)

    created_date = models.DateTimeField(
        auto_now_add=True)

    modified_date = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return f'Review Response for Review: {self.review.id}'

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Review Response")
        verbose_name_plural = _("Review Responses")

        ordering = ['-created_date']
