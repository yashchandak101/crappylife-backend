# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def assign_default_permissions(sender, instance, created, **kwargs):
    if created:
        # Assign basic permissions or groups if needed
        pass
