from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import User

# Match with roles.py constants
ROLE_AUTHORS = "Author"
ROLE_EDITORS = "Editor"
ROLE_ADMINS = "Admin"


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "role", "get_roles", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")

    # Custom fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "bio", "profile_image")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("role", "bio", "profile_image")}),
    )

    def get_queryset(self, request):
        """
        Filter queryset based on user role.
        Superusers and Admins see all users.
        Others see only themselves.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name=ROLE_ADMINS).exists():
            return qs
        return qs.filter(id=request.user.id)

    def has_module_permission(self, request):
        """
        Allow staff users to see this module in admin.
        This is crucial for staff members to see the User section.
        """
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        """Allow staff to view users"""
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            # Staff can view themselves or if they're admin/editor
            if obj is None:
                return True
            if obj == request.user:
                return True
            return request.user.groups.filter(name__in=[ROLE_ADMINS, ROLE_EDITORS]).exists()
        return False

    def has_change_permission(self, request, obj=None):
        """Control who can change users"""
        if request.user.is_superuser:
            return True
        if obj is None:
            # For the changelist
            return request.user.groups.filter(name__in=[ROLE_ADMINS, ROLE_EDITORS]).exists()
        # Can change own profile
        if obj == request.user:
            return True
        # Only admins and editors can change other users
        return request.user.groups.filter(name__in=[ROLE_ADMINS, ROLE_EDITORS]).exists()

    # Display groups (roles) in admin list
    def get_roles(self, obj):
        roles = [g.name for g in obj.groups.all()]
        return ", ".join(roles) if roles else "-"
    get_roles.short_description = "Groups"

    # Admin actions to assign roles quickly
    @admin.action(description="Assign Author role")
    def make_author(self, request, queryset):
        self.assign_role(request, queryset, ROLE_AUTHORS, "author")

    @admin.action(description="Assign Editor role")
    def make_editor(self, request, queryset):
        self.assign_role(request, queryset, ROLE_EDITORS, "editor")

    @admin.action(description="Assign Admin role")
    def make_admin(self, request, queryset):
        self.assign_role(request, queryset, ROLE_ADMINS, "admin")

    def get_actions(self, request):
        """Only show role assignment actions to admins"""
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if not request.user.groups.filter(name=ROLE_ADMINS).exists():
                # Remove role assignment actions for non-admins
                actions.pop('make_author', None)
                actions.pop('make_editor', None)
                actions.pop('make_admin', None)
        return actions

    # Shared role assignment logic
    def assign_role(self, request, queryset, role_name, role_field_value):
        """Assign role to selected users and set up permissions"""
        group, _ = Group.objects.get_or_create(name=role_name)

        # Define permissions for each role
        if role_name == "Author":
            # Authors can view and manage their own content
            perm_codenames = [
                'view_article', 'add_article', 'change_article',
                'view_user',  # Can view user list
            ]
            perms = Permission.objects.filter(codename__in=perm_codenames)
        elif role_name == "Editor":
            # Editors can manage all content
            perm_codenames = [
                'view_article', 'add_article', 'change_article', 'delete_article',
                'view_user', 'change_user',
            ]
            perms = Permission.objects.filter(codename__in=perm_codenames)
        elif role_name == "Admin":
            # Admins get all permissions
            perms = Permission.objects.all()
        else:
            perms = []

        # Assign the permissions to the group
        group.permissions.set(perms)

        # Add users to the group and update their role field
        count = 0
        for user in queryset:
            user.groups.clear()  # Remove from other role groups
            user.groups.add(group)
            user.role = role_field_value
            
            # Set staff/superuser status
            if role_name == "Admin":
                user.is_staff = True
                user.is_superuser = True
            elif role_name in ["Author", "Editor"]:
                user.is_staff = True
                user.is_superuser = False
            
            user.save()
            count += 1

        messages.success(
            request, 
            f"✓ Assigned {role_name} role to {count} user(s). They now have {perms.count()} permissions."
        )

    @admin.action(description="🔧 FIX: Force Superuser Access")
    def force_superuser(self, request, queryset):
        """Emergency fix for admin access issues"""
        from django.contrib.auth.models import Group
        
        count = 0
        for user in queryset:
            # Force all flags
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.role = 'admin'
            user.save()
            
            # Add to Admin group
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            user.groups.clear()
            user.groups.add(admin_group)
            
            count += 1
        
        messages.success(
            request,
            f"✓ Fixed {count} user(s) - They are now superusers. Ask them to log out and log back in."
        )
    
    actions = ["make_author", "make_editor", "make_admin", "force_superuser"]


# Clean Group admin view
admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "get_permissions_count", "get_users_count")
    search_fields = ("name",)
    filter_horizontal = ("permissions",)
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()
    get_permissions_count.short_description = "Permissions"
    
    def get_users_count(self, obj):
        return obj.user_set.count()
    get_users_count.short_description = "Users"
    
    def has_module_permission(self, request):
        """Allow staff to see groups"""
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name__in=[ROLE_ADMINS, ROLE_EDITORS]).exists()