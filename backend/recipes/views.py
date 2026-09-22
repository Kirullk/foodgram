from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response

from core.filters import RecipeFilter
from core.mixins import ListRetrieveMixin, RecipeRelationMixin
from core.pagination import RecipePagination
from core.permission import IsAuthorOrReadOnly
from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeCreateSerializer, RecipeSerializer, TagSerializer


class TagViewSet(ListRetrieveMixin):
    """Вьюсет для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveMixin):
    """Вьюсет для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class FavoriteViewSet(RecipeRelationMixin):

    relation_field = 'favorites'
    error_exists = 'Данный рецепт уже добавлен'
    error_not_exists = 'Объект уже удален из избранных'

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, pk=None):
        return self.toggle_relation(request, pk)


class CartViewSet(RecipeRelationMixin):

    relation_field = 'shopping_cart'
    error_exists = 'Данный рецепт уже добавлен'
    error_not_exists = 'Объект уже удален из списка покупок'

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        return self.toggle_relation(request, pk)


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch',
                         'delete', 'head', 'options')
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.getlist('tags')
        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('get',), url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_link = request.build_absolute_uri(f'/s/{recipe.short_code}')
        return Response({'short-link': short_link}, status=status.HTTP_200_OK)

    @action(detail=False, methods=('get',))
    def download_shopping_cart(self, request):
        recipes = request.user.shopping_cart.prefetch_related(
            'recipe_ingredients__ingredient'
        )
        totals = dict()
        for recipe in recipes:
            for ingr in recipe.recipe_ingredients.all():
                key = (ingr.ingredient.name, ingr.ingredient.measurement_unit)
                totals[key] = totals.get(key, 0) + ingr.amount
        lines = ['Список покупок:', '']
        for (name, unit), amount in totals.items():
            lines.append(f'{name}. {amount} ({unit})')
        content = '\n'.join(lines)

        response = HttpResponse(
            content,
            content_type='text/plain; charset=utf-8'
        )
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        return response


def short_link_redirect(request, code):
    recipe = get_object_or_404(Recipe, short_code=code)
    return redirect(f'/recipes/{recipe.id}/')
