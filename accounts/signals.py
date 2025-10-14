from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

@receiver(post_save, sender=User)
def set_user_permissions(sender, instance, created, **kwargs):
    """
    Automatically assign group and permissions based on user role.
    """
    if created:
        # Prevent recursion by using update instead of save
        update_fields = {}
        
        # Set staff/superuser status based on role
        if instance.role == "admin":
            update_fields['is_staff'] = True
            update_fields['is_superuser'] = True
            group_name = "Admin"
        elif instance.role in ["author", "editor"]:
            update_fields['is_staff'] = True
            group_name = "Author" if instance.role == "author" else "Editor"
        else:
            group_name = None
        
        # Update user without triggering signal again
        if update_fields:
            User.objects.filter(pk=instance.pk).update(**update_fields)
        
        # Add user to appropriate group
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)