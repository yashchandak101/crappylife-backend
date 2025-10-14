from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from .models import User
from .roles import ROLE_AUTHORS, ROLE_EDITORS, ROLE_ADMINS  # if you have a roles.py


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Fields to display in the user list
    list_display = ("id", "username", "email", "get_roles", "is_staff", "is_active", "bio")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")

    # Add custom fields (bio, profile_image)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("bio", "profile_image")}),
    )

    # Fields when creating a new user
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("bio", "profile_image")}),
    )

    # ✅ Display user roles (groups) in admin list
    def get_roles(self, obj):
        roles = [g.name for g in obj.groups.all()]
        if not roles:
            return "-"
        return ", ".join(roles)
    get_roles.short_description = "Roles"

    # ✅ Custom actions to assign roles easily
    @admin.action(description="Assign Author role")
    def make_author(self, request, queryset):
        self.assign_role(request, queryset, ROLE_AUTHORS)

    @admin.action(description="Assign Editor role")
    def make_editor(self, request, queryset):
        self.assign_role(request, queryset, ROLE_EDITORS)

    @admin.action(description="Assign Admin role")
    def make_admin(self, request, queryset):
        self.assign_role(request, queryset, ROLE_ADMINS)

    def assign_role(self, request, queryset, role_name):
        group, _ = Group.objects.get_or_create(name=role_name)
        for user in queryset:
            user.groups.add(group)
        messages.success(request, f"Assigned {role_name} role to selected users.")

    actions = ["make_author", "make_editor", "make_admin"]


# ✅ Custom Group admin (optional but cleaner)
admin.site.unregister(Group)
@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
