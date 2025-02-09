from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        """
        Automatically set is_staff based on role:
        - Admin users -> is_staff=True
        - Normal users -> is_staff=False
        """
        if self.role == "admin":
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
