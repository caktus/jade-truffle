from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from model_utils.models import TimeStampedModel
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email
