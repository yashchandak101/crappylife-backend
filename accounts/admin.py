from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

# Optional: define roles here if you don’t have roles.py
ROLE_AUTHORS = "author"
ROLE_EDITORS = "editor"
ROLE_ADMINS = "admin"


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")

    # ✅ Custom fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "bio", "profile_image")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("role", "bio", "profile_image")}),
    )

    # ✅ Display groups (roles) in admin list
    def get_roles(self, obj):
        roles = [g.name for g in obj.groups.all()]
        return ", ".join(roles) if roles else "-"
    get_roles.short_description = "Groups"

    # ✅ Admin actions to assign roles quickly
    @admin.action(description="Assign Author role")
    def make_author(self, request, queryset):
        self.assign_role(request, queryset, ROLE_AUTHORS)

    @admin.action(description="Assign Editor role")
    def make_editor(self, request, queryset):
        self.assign_role(request, queryset, ROLE_EDITORS)

    @admin.action(description="Assign Admin role")
    def make_admin(self, request, queryset):
        self.assign_role(request, queryset, ROLE_ADMINS)

    # ✅ Shared role assignment logic
    def assign_role(self, request, queryset, role_name):
        group, _ = Group.objects.get_or_create(name=role_name)
        for user in queryset:
            user.role = role_name  # update User.role field
            user.groups.clear()  # optional: clear existing groups
            user.groups.add(group)
            user.save()
        messages.success(request, f"Assigned '{role_name}' role to selected users.")

    actions = ["make_author", "make_editor", "make_admin"]


# ✅ Optional: Clean Group admin view
admin.site.unregister(Group)

@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
