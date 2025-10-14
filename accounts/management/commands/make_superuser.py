# accounts/management/commands/make_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = 'Make an existing user a superuser'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to make superuser')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Make superuser
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.role = 'admin'  # Set role to admin
            user.save()
            
            # Add to Admin group
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            user.groups.clear()  # Remove from other groups
            user.groups.add(admin_group)
            
            self.stdout.write(self.style.SUCCESS('\n' + '='*60))
            self.stdout.write(self.style.SUCCESS(f'✓ Successfully made {username} a superuser!'))
            self.stdout.write(self.style.SUCCESS('='*60))
            self.stdout.write(f'Username:    {user.username}')
            self.stdout.write(f'Email:       {user.email}')
            self.stdout.write(f'Role:        {user.role}')
            self.stdout.write(f'Staff:       {user.is_staff}')
            self.stdout.write(f'Superuser:   {user.is_superuser}')
            self.stdout.write(f'Active:      {user.is_active}')
            self.stdout.write(f'Groups:      {", ".join([g.name for g in user.groups.all()])}')
            self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'\n✗ User "{username}" does not exist!\n'))
            self.stdout.write(self.style.WARNING('Available users:'))
            for u in User.objects.all():
                groups = ', '.join([g.name for g in u.groups.all()]) or 'None'
                self.stdout.write(
                    f'  • {u.username:<20} | Role: {u.role:<10} | '
                    f'Staff: {str(u.is_staff):<5} | Groups: {groups}'
                )
            self.stdout.write('')