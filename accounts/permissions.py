# core/permissions.py
from rest_framework import permissions
from .roles import is_author, is_editor, is_admin

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow full access to object author; read-only for others.
    Assumes view.get_object() returns object with `.author` attribute.
    """

    def has_permission(self, request, view):
        # Allow list and create for authenticated users (create will set author)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow if the request user is the author
        return getattr(obj, "author", None) == request.user or is_admin(request.user) or is_editor(request.user)


class IsEditorOrAdmin(permissions.BasePermission):
    """
    Allow editors and admins full access, others read-only.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return is_editor(request.user) or is_admin(request.user)


class IsAuthorEditorAdminOrReadOnly(permissions.BasePermission):
    """
    Combined: authors (object owner), editors, admins can modify; others read-only.
    """

    def has_permission(self, request, view):
        # Allow read for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # For non-safe methods, must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Editors and admins can do anything
        if is_editor(request.user) or is_admin(request.user):
            return True
        # Authors can act on their own objects
        return getattr(obj, "author", None) == request.user
