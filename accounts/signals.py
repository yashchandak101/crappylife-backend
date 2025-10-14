from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.utils import OperationalError, ProgrammingError


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    """Create Author, Editor, and Admin groups with proper permissions."""
    if sender.name != "accounts":
        return  # run only once for the accounts app

    try:
        from articles.models import Article  # safe to import now

        # Author
        author_group, _ = Group.objects.get_or_create(name="Author")
        author_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Article),
            codename__in=["add_article", "change_article", "view_article"],
        )
        author_group.permissions.set(author_perms)
        author_group.save()

        # Editor
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Article),
            codename__in=["add_article", "change_article", "delete_article", "view_article"],
        )
        editor_group.permissions.set(editor_perms)
        editor_group.save()

        # Admin
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        admin_group.permissions.set(Permission.objects.all())
        admin_group.save()

        print("✅ Default roles created successfully")

    except (OperationalError, ProgrammingError):
        # Happens if DB tables aren’t created yet (first migrate)
        pass
