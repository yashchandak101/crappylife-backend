from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from django.db.models.signals import post_migrate
        from accounts import signals  # Lazy import

        post_migrate.connect(signals.create_default_roles, dispatch_uid="create_default_roles_safe")