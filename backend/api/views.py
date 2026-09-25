from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import Pagination
from api.permission import IsAuthorOrReadOnly
from recipes.models import (Favorite, Follow, Ingredient,
                            Recipe, ShoppingCart, Tag)
from .serializers import (AvatarSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShortRecipeSerializer, SubscriptionSerializer,
                          TagSerializer)


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет пользователей."""

    pagination_class = Pagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            return (AllowAny(),)
        return (IsAuthenticated(),)

    @action(detail=False, methods=('put', 'delete'), url_path='me/avatar')
    def avatar(self, request):
        if request.method == 'PUT':
            serializer = AvatarSerializer(
                instance=request.user,
                data=request.data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=('get',), url_path='subscriptions')
    def subscriptions(self, request):
        authors = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(authors)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('post', 'delete'))
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if author == request.user:
                return Response(
                    {'error': 'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Follow.objects.filter(
                user=request.user, author=author
            ).exists():
                return Response(
                    {'error': 'Вы уже подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Follow.objects.create(user=request.user, author=author)
            serializer = SubscriptionSerializer(
                author, context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not Follow.objects.filter(user=request.user, author=author).exists():
            return Response(
                {'error': 'Вы не подписаны на данного пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.get(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user,
                                       recipe=recipe).exists():
                return Response(
                    {'error': 'Данный рецепт уже добавлен'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favorite.objects.create(user=request.user,
                                    recipe=recipe)
            return Response(
                ShortRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED,
            )

        if not Favorite.objects.filter(user=request.user,
                                       recipe=recipe).exists():
            return Response(
                {'error': 'Данный рецепт отсутствует в списке'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Favorite.objects.get(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                return Response(
                    {'error': 'Данный рецепт уже добавлен'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.create(user=request.user,
                                        recipe=recipe)
            return Response(
                ShortRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED,
            )

        if not ShoppingCart.objects.filter(user=request.user,
                                           recipe=recipe).exists():
            return Response(
                {'error': 'Данный рецепт отсутствует в списке'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ShoppingCart.objects.get(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('get',), url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_link = request.build_absolute_uri(f'/s/{recipe.short_code}')
        return Response(
            {'short-link': short_link},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=('get',))
    def download_shopping_cart(self, request):
        recipes = Recipe.objects.filter(
            in_carts__user=request.user
        ).prefetch_related('recipe_ingredients__ingredient')

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
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (AllowAny,)


def short_link_redirect(request, code):
    """Редирект по короткой ссылке на рецепт."""

    recipe = get_object_or_404(Recipe, short_code=code)
    return redirect(f'/recipes/{recipe.id}/')
