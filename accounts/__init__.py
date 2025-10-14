from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from articles.models import Article  # adjust if your model name or app differs

class Command(BaseCommand):
    help = "Setup default roles and permissions"

    def handle(self, *args, **options):
        # Author
        author_group, _ = Group.objects.get_or_create(name='Author')
        author_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Article),
            codename__in=['add_article', 'change_article', 'view_article']
        )
        author_group.permissions.set(author_perms)
        author_group.save()

        # Editor
        editor_group, _ = Group.objects.get_or_create(name='Editor')
        editor_perms = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Article),
            codename__in=['change_article', 'view_article', 'delete_article']
        )
        editor_group.permissions.set(editor_perms)
        editor_group.save()

        # Admin
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        admin_group.permissions.set(Permission.objects.all())
        admin_group.save()

        self.stdout.write(self.style.SUCCESS("✅ Roles & permissions created successfully!"))
