# accounts/management/commands/create_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from articles.models import Article

class Command(BaseCommand):
    help = "Create user role groups (Author, Editor, Admin) and assign basic permissions."

    def handle(self, *args, **options):
        groups = ["Author", "Editor", "Admin"]
        for g in groups:
            group, created = Group.objects.get_or_create(name=g)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {g}"))
            else:
                self.stdout.write(self.style.WARNING(f"Group already exists: {g}"))

        # Example: give Editor permission to change Article
        ct = ContentType.objects.get_for_model(Article)
        change_article = Permission.objects.get(codename="change_article", content_type=ct)
        publish_perm, _ = Permission.objects.get_or_create(codename="can_publish_article", name="Can publish article", content_type=ct)

        editor_group = Group.objects.get(name="Editor")
        editor_group.permissions.add(change_article, publish_perm)

        admin_group = Group.objects.get(name="Admin")
        # give admin all article perms
        perms = Permission.objects.filter(content_type=ct)
        admin_group.permissions.set(list(perms))

        self.stdout.write(self.style.SUCCESS("Finished setting up role groups and permissions."))
