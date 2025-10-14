from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def set_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.role == "Admin":
            instance.is_staff = True
            instance.is_superuser = True
        elif instance.role in ["Author", "Editor"]:
            instance.is_staff = True
        instance.save()