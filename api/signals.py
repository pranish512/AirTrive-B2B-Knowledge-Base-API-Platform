import secrets
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Company
@receiver(pre_save, sender=User)
def remember_user_adding(sender, instance, **kwargs):
    # Assignment explicitly asks for instance._state.adding to detect first creation.
    instance._teamboard_was_adding = instance._state.adding
@receiver(post_save, sender=User)
def create_company_profile(sender, instance, created, **kwargs):
    if getattr(instance, '_teamboard_was_adding', created):
        Company.objects.get_or_create(user=instance, defaults={'company_name': instance.email or instance.username, 'api_key': secrets.token_urlsafe(32)})
