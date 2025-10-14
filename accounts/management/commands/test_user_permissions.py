# accounts/management/commands/test_user_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

User = get_user_model()


class Command(BaseCommand):
    help = 'Test and display user permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to check (optional, shows all if not provided)'
        )

    def handle(self, *args, **kwargs):
        username = kwargs.get('username')
        
        if username:
            try:
                users = [User.objects.get(username=username)]
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" not found!'))
                return
        else:
            users = User.objects.all()
        
        for user in users:
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.SUCCESS(f'👤 User: {user.username}'))
            self.stdout.write('='*60)
            
            # Basic info
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Role: {user.role}')
            self.stdout.write(f'Staff: {user.is_staff}')
            self.stdout.write(f'Superuser: {user.is_superuser}')
            self.stdout.write(f'Active: {user.is_active}')
            
            # Groups
            groups = user.groups.all()
            self.stdout.write(f'\n📋 Groups ({groups.count()}):')
            if groups:
                for group in groups:
                    self.stdout.write(f'  • {group.name}')
            else:
                self.stdout.write(self.style.WARNING('  ⚠ No groups assigned!'))
            
            # Permissions
            self.stdout.write(f'\n🔐 Permissions:')
            
            # Group permissions
            group_perms = Permission.objects.filter(group__user=user).distinct()
            self.stdout.write(f'  From Groups ({group_perms.count()}):')
            if group_perms:
                for perm in group_perms:
                    self.stdout.write(f'    • {perm.codename} ({perm.content_type})')
            else:
                self.stdout.write(self.style.WARNING('    ⚠ No group permissions!'))
            
            # Direct permissions
            user_perms = user.user_permissions.all()
            if user_perms:
                self.stdout.write(f'  Direct ({user_perms.count()}):')
                for perm in user_perms:
                    self.stdout.write(f'    • {perm.codename}')
            
            # Check admin access
            self.stdout.write(f'\n🔓 Admin Access:')
            self.stdout.write(f'  Can access admin: {user.is_staff}')
            self.stdout.write(f'  Has view_user: {user.has_perm("accounts.view_user")}')
            self.stdout.write(f'  Has change_user: {user.has_perm("accounts.change_user")}')
            
            # Problem detection
            if user.is_staff and group_perms.count() == 0 and not user.is_superuser:
                self.stdout.write(
                    self.style.ERROR(
                        '\n❌ PROBLEM: User is staff but has no permissions!'
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        '   → Run: python manage.py setup_roles'
                    )
                )
        
        self.stdout.write('\n' + '='*60 + '\n')