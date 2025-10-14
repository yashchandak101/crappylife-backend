# accounts/management/commands/fix_my_admin.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix admin access for your user - makes you a superuser'

    def handle(self, *args, **kwargs):
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.WARNING('FIXING ADMIN ACCESS'))
        self.stdout.write('='*70 + '\n')
        
        # Show all users
        self.stdout.write(self.style.SUCCESS('Available users:'))
        users = User.objects.all()
        
        for i, user in enumerate(users, 1):
            status = '✓ Superuser' if user.is_superuser else ('✓ Staff' if user.is_staff else '✗ No access')
            self.stdout.write(f'{i}. {user.username:<20} | {status}')
        
        if not users:
            self.stdout.write(self.style.ERROR('No users found! Create one with: python manage.py createsuperuser'))
            return
        
        self.stdout.write('')
        
        # Get user choice
        try:
            choice = input('Enter the number of user to fix (or username): ').strip()
            
            # Try as number first
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(users):
                    user = list(users)[choice_num - 1]
                else:
                    self.stdout.write(self.style.ERROR(f'Invalid number. Choose 1-{len(users)}'))
                    return
            except ValueError:
                # Try as username
                try:
                    user = User.objects.get(username=choice)
                except User.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'User "{choice}" not found!'))
                    return
            
            # Show before status
            self.stdout.write('')
            self.stdout.write(self.style.WARNING(f'BEFORE - {user.username}:'))
            self.stdout.write(f'  is_active:    {user.is_active}')
            self.stdout.write(f'  is_staff:     {user.is_staff}')
            self.stdout.write(f'  is_superuser: {user.is_superuser}')
            self.stdout.write(f'  role:         {user.role}')
            self.stdout.write(f'  groups:       {", ".join([g.name for g in user.groups.all()]) or "None"}')
            
            # Fix the user
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.role = 'admin'
            user.save()
            
            # Add to Admin group
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            user.groups.clear()
            user.groups.add(admin_group)
            
            # Show after status
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS(f'AFTER - {user.username}:'))
            self.stdout.write(f'  is_active:    {user.is_active} ✓')
            self.stdout.write(f'  is_staff:     {user.is_staff} ✓')
            self.stdout.write(f'  is_superuser: {user.is_superuser} ✓')
            self.stdout.write(f'  role:         {user.role}')
            self.stdout.write(f'  groups:       {", ".join([g.name for g in user.groups.all()])}')
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('='*70))
            self.stdout.write(self.style.SUCCESS('✓ FIXED! Now do this:'))
            self.stdout.write(self.style.SUCCESS('  1. Log out from Django admin'))
            self.stdout.write(self.style.SUCCESS('  2. Log back in'))
            self.stdout.write(self.style.SUCCESS('  3. You should now see everything!'))
            self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
            
        except KeyboardInterrupt:
            self.stdout.write('\n\nCancelled.')
            return