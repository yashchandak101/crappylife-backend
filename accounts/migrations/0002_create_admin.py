# accounts/migrations/0002_create_admin.py
from django.db import migrations

def create_admin(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.create_superuser(
        username="yashsuper",
        email="channdak.yash101@gmail.com",
        password="Yash@123"
    )

class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
