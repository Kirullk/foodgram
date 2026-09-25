import django_filters

from recipes.models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    """Фильтр ингредиентов по началу названия."""

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр рецептов."""

    author = django_filters.NumberFilter(field_name='author_id')
    is_favorited = django_filters.NumberFilter(method='filter_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_in_cart'
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value == 1:
            return queryset.filter(favorited_by__user=self.request.user)
        return queryset

    def filter_in_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value == 1:
            return queryset.filter(in_carts__user=self.request.user)
        return queryset
