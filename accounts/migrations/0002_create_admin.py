from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    Permission = apps.get_model("auth", "Permission")

    # Create only if not exists
    if not User.objects.filter(username="yashchandak").exists():
        user = User.objects.create_superuser(
            username="yashchandak",
            email="yashchandakk.01@gmail.com",
            password="yashchandak123"
        )
        # Explicitly make sure
        user.is_staff = True
        user.is_superuser = True
        user.save()

        # Assign all permissions
        all_permissions = Permission.objects.all()
        user.user_permissions.set(all_permissions)
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
