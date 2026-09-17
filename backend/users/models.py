from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя."""

    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        verbose_name='Подписки'
    ),
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        blank=True,
        related_name='favorited_by',
        verbose_name='Избранное',
    )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        blank=True,
        related_name='in_carts',
        verbose_name='Список покупок'
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='users/',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
