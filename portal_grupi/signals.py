from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Group.objects.get_or_create(name='user')
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.role = 'user'
        profile.full_name = f"{instance.first_name} {instance.last_name}".strip()
        profile.save()
    else:
        Profile.objects.get_or_create(user=instance)
