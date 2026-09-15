from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_subscribed = models.BooleanField(
        default=False
    )
    avatar = models.ImageField(
        upload_to='users/',
        null=True,
        blank=True
    )
