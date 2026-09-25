import secrets

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from api.constants import (INGREDIENT_NAME_MAX_LENGTH,
                           MEASUREMENT_UNIT_MAX_LENGTH,
                           MIN_AMOUNT, MIN_COOKING_TIME,
                           RECIPE_NAME_MAX_LENGTH, SHORT_CODE_MAX_LENGTH,
                           TAG_MAX_LENGTH)


User = get_user_model()


class Tag(models.Model):
    """Модель Тега."""

    name = models.CharField(
        'Название',
        max_length=TAG_MAX_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=TAG_MAX_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель Ингредиента."""

    name = models.CharField(
        'Название',
        max_length=INGREDIENT_NAME_MAX_LENGTH,
        unique=True,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MEASUREMENT_UNIT_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    name = models.CharField(
        'Название',
        max_length=RECIPE_NAME_MAX_LENGTH,
    )
    text = models.TextField(
        'Описание',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (мин)',
        validators=[MinValueValidator(MIN_COOKING_TIME)],
    )
    short_code = models.CharField(
        'Короткая ссылка',
        max_length=SHORT_CODE_MAX_LENGTH,
        unique=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = secrets.token_urlsafe(4)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель Ингредиента в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(MIN_AMOUNT)],
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ('recipe__name',)

    def __str__(self):
        return f'{self.ingredient.name} в {self.recipe.name}'


class Favorite(models.Model):
    """Избранные рецепты пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite',
            ),
        ]

    def __str__(self):
        return f'{self.user} → {self.recipe}'


class ShoppingCart(models.Model):
    """Список покупок пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_carts',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        ]

    def __str__(self):
        return f'{self.user} → {self.recipe}'


class Follow(models.Model):
    """Подписки пользователя на авторов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow',
            ),
            models.CheckConstraint(
                condition=~models.Q(user=models.F('author')),
                name='prevent_self_follow',
            ),
        ]

    def __str__(self):
        return f'{self.user} → {self.author}'
