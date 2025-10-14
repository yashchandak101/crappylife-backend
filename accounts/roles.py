from django.contrib.auth import get_user_model

User = get_user_model()

ROLE_AUTHORS = "Author"
ROLE_EDITORS = "Editor"
ROLE_ADMINS = "Admin"

def in_group(user, group_name: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()

def is_author(user) -> bool:
    return in_group(user, ROLE_AUTHORS)

def is_editor(user) -> bool:
    return in_group(user, ROLE_EDITORS)

def is_admin(user) -> bool:
    # treat Django superuser or group 'Admin' as admin
    return user.is_superuser or in_group(user, ROLE_ADMINS)
