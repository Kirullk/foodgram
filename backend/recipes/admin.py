from django.contrib import admin

from .models import Ingredient, Tag, Recipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_name')
    search_fields = ('name', 'author__first_name')
    list_filter = ('tags',)
    readonly_fields = ('favorites_count',)

    def author_name(self, obj):
        return obj.author.first_name
    author_name.short_description = 'Автор'

    def favorites_count(self, obj):
        return obj.favorited_by.count()
    favorites_count.short_description = 'В избранном'
