# accounts/management/commands/setup_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class Command(BaseCommand):
    help = 'Setup user roles and permissions for the news website'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Setting up roles and permissions...\n'))
        
        # Get all available models for permissions
        all_models = apps.get_models()
        
        # Define roles and their permissions
        roles_config = {
            'Author': {
                'description': 'Can create and edit their own articles and events',
                'permissions': [
                    # Article permissions
                    'view_article',
                    'add_article',
                    'change_article',
                    # Event permissions
                    'view_event',
                    'add_event',
                    'change_event',
                    # Category and Tag permissions
                    'view_category',
                    'view_tag',
                    # User permissions (view only)
                    'view_user',
                ]
            },
            'Editor': {
                'description': 'Can manage all articles, events, and content',
                'permissions': [
                    # Article permissions
                    'view_article',
                    'add_article',
                    'change_article',
                    'delete_article',
                    # Event permissions
                    'view_event',
                    'add_event',
                    'change_event',
                    'delete_event',
                    # Category and Tag permissions
                    'view_category',
                    'add_category',
                    'change_category',
                    'delete_category',
                    'view_tag',
                    'add_tag',
                    'change_tag',
                    'delete_tag',
                    # User permissions
                    'view_user',
                    'change_user',
                ]
            },
            'Admin': {
                'description': 'Full access to everything',
                'permissions': 'all'
            }
        }

        for role_name, config in roles_config.items():
            group, created = Group.objects.get_or_create(name=role_name)
            
            if config['permissions'] == 'all':
                # Give all permissions to Admin
                all_perms = Permission.objects.all()
                group.permissions.set(all_perms)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {role_name}: {config["description"]}'
                    )
                )
                self.stdout.write(f'  → ALL permissions ({all_perms.count()} total)\n')
            else:
                # Get specific permissions - be flexible if they don't exist yet
                permissions = Permission.objects.filter(codename__in=config['permissions'])
                group.permissions.set(permissions)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ {role_name}: {config["description"]}'
                    )
                )
                self.stdout.write(f'  → {permissions.count()} permissions assigned:')
                for perm in permissions:
                    self.stdout.write(f'    • {perm.codename} ({perm.content_type})')
                
                # Warn about missing permissions
                missing = set(config['permissions']) - set(permissions.values_list('codename', flat=True))
                if missing:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ Missing permissions (create models first): {", ".join(missing)}')
                    )
                self.stdout.write('')

        self.stdout.write(self.style.SUCCESS('✅ Role setup complete!\n'))
        
        # Show current state
        self.stdout.write(self.style.WARNING('Current Groups and Permissions:'))
        for group in Group.objects.all():
            self.stdout.write(f'\n📋 {group.name}:')
            perms = group.permissions.all()
            if perms.count() > 10:
                self.stdout.write(f'  → {perms.count()} permissions (too many to list)')
            else:
                for perm in perms:
                    self.stdout.write(f'  • {perm.codename}')