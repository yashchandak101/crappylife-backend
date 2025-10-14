from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("author", "Author"),
        ("editor", "Editor"),
        ("admin", "Admin"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="author")
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="users/", blank=True, null=True)

    def __str__(self):
        return self.username
