from profiles.models import Profile
from reviews.services import profile_update_rating_numbers
from reviews.models import Review
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates user Profile
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves user Profile
    """
    instance.profile.save()


@receiver(post_save, sender=Review)
def update_review_figures(sender, instance, **kwargs):
    """
    Update User Rating on Profile
    """
    profile_update_rating_numbers(instance)


@receiver(post_delete, sender=Review)
def update_review_figures_delete(sender, instance, **kwargs):
    """
    Update User Rating on Profile
    """
    profile_update_rating_numbers(instance)
