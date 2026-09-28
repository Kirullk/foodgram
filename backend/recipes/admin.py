from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Favorite, Ingredient, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


class RecipeIngredientInline(admin.TabularInline):
    """Инлайн ингредиентов внутри рецепта."""

    model = RecipeIngredient
    extra = 1
    min_num = 1
    validate_min = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    list_display = (
        'id', 'name', 'author_link', 'cooking_time',
        'tags_list', 'ingredients_list', 'image_preview',
        'favorites_count',
    )
    search_fields = ('name', 'author__first_name', 'author__email')
    list_filter = ('tags', 'author')
    readonly_fields = ('favorites_count', 'image_preview')
    inlines = (RecipeIngredientInline,)

    @admin.display(description='Автор')
    def author_link(self, obj):
        url = f'/admin/users/user/{obj.author.id}/change/'
        return mark_safe(f'<a href="{url}">{obj.author.username}</a>')

    @admin.display(description='Теги')
    def tags_list(self, obj):
        return ', '.join(tag.name for tag in obj.tags.all())

    @admin.display(description='Ингредиенты')
    def ingredients_list(self, obj):
        return ', '.join(f'{ri.ingredient.name} — {ri.amount}'
                         for ri in obj.recipe_ingredients.all())

    @admin.display(description='Картинка')
    def image_preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="80" height="60">'
        )

    @admin.display(description='В избранном')
    def favorites_count(self, obj):
        return obj.favorites.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка избранного."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
    list_filter = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка списка покупок."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
    list_filter = ('user',)
