from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the user list
    list_display = ("id", "username", "email", "is_staff", "is_active", "bio")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")

    # Fields in the form when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("bio", "profile_image")}),
    )

    # Fields when creating a new user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("bio", "profile_image")}),
    )
