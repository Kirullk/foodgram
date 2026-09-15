from django.db import models


class Tag(models.Model):
    """Модель Тега."""

    name = models.CharField(
        'Название', max_length=150, unique=True
    )
    slug = models.SlugField(
        'Слаг', max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'Тег {self.name}'


class Ingredient(models.Model):
    """Модель Ингредиента."""

    name = models.CharField(
        'Название', max_length=150, unique=True
    )
    measurement_unit = models.PositiveSmallIntegerField(
        'Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'Ингредиент {self.name}'
