from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    """Инлайн ингредиентов внутри рецепта."""

    model = RecipeIngredient
    extra = 1
    min_num = 1
    validate_min = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    list_display = ('id', 'name', 'author_name', 'cooking_time')
    search_fields = ('name', 'author__first_name')
    list_filter = ('tags',)
    readonly_fields = ('favorites_count',)
    inlines = (RecipeIngredientInline,)

    def author_name(self, obj):
        return obj.author.first_name
    author_name.short_description = 'Автор'

    def favorites_count(self, obj):
        return obj.favorited_by.count()
    favorites_count.short_description = 'В избранном'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка избранного."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка списка покупок."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админка подписок."""

    list_display = ('id', 'user', 'author')
    search_fields = ('user__username', 'author__username')
