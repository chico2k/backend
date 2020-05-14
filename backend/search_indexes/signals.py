from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

__all__ = (
    'update_document',
    'delete_document',
)


@receiver(post_save)
def update_document(sender, **kwargs):
    # from profiles.models import Profile

    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    registry.update(instance)

    if app_label == 'sports':
        if model_name == 'sport':
            registry.update(instance.profile)
    elif app_label == 'location':
        if model_name == 'location':
            registry.update(instance.profile)
    elif app_label == 'reviews':
        if model_name == 'review':
            registry.update(instance)
            registry.update(instance.profile)


@receiver(post_delete)
def delete_document(sender, **kwargs):

    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'sports':
        if model_name == 'sport':
            registry.update(instance.profile)
    elif app_label == 'location':
        if model_name == 'location':
            registry.update(instance.profile)
    elif app_label == 'reviews':
        if model_name == 'review':
            registry.update(instance)
            registry.update(instance.profile)
