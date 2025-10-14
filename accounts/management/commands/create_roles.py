# accounts/management/commands/setup_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Setup user roles and permissions for the news website'

    def handle(self, *args, **kwargs):
        # Define roles and their permissions
        roles_permissions = {
            'Author': [
                'view_article',
                'add_article',
                'change_article',
            ],
            'Editor': [
                'view_article',
                'add_article',
                'change_article',
                'delete_article',
            ],
            'Admin': 'all',  # Special case for all permissions
        }

        for role_name, perms in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role_name)
            
            if perms == 'all':
                # Give all permissions to Admin
                all_perms = Permission.objects.all()
                group.permissions.set(all_perms)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {role_name} group created/updated with ALL permissions')
                )
            else:
                # Get specific permissions
                permissions = Permission.objects.filter(codename__in=perms)
                group.permissions.set(permissions)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {role_name} group created/updated with {permissions.count()} permissions'
                    )
                )

        self.stdout.write(self.style.SUCCESS('\n✅ Role setup complete!'))
        self.stdout.write(self.style.WARNING(
            '\nNote: Make sure your Article model exists and has migrations applied.'
        ))