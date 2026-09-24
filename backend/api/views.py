from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.filters import RecipeFilter
from api.mixins import ListRetrieveMixin, RecipeRelationMixin
from api.pagination import RecipePagination, UserPagination
from api.permission import IsAuthorOrReadOnly
from recipes.models import Ingredient, Recipe, Tag

from .serializers import (AvatarSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          SubscriptionSerializer, TagSerializer)


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет пользователей."""

    pagination_class = UserPagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            return (AllowAny(),)
        return (IsAuthenticated(),)


class AvatarViewSet(GenericViewSet):
    """Вьюсет аватара пользователя."""

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


class SubscribeViewSet(GenericViewSet):
    """Вьюсет подписок."""

    pagination_class = UserPagination

    @action(detail=False, methods=('get',), url_path='subscriptions')
    def subscriptions(self, request):
        subs = request.user.subscriptions.all()
        page = self.paginate_queryset(subs)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('post', 'delete'))
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        subscriptions = request.user.subscriptions

        if request.method == 'POST':
            if author == request.user:
                return Response(
                    {'error': 'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if subscriptions.filter(id=author.id).exists():
                return Response(
                    {'error': 'Вы уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscriptions.add(author)
            serializer = SubscriptionSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not subscriptions.filter(id=author.id).exists():
            return Response(
                {'error': 'Вы не подписаны'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscriptions.remove(author)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""

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
        return queryset

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
        return Response(
            {'short-link': short_link},
            status=status.HTTP_200_OK,
        )

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
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response


class TagViewSet(ListRetrieveMixin):
    """Вьюсет тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveMixin):
    """Вьюсет ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class FavoriteViewSet(RecipeRelationMixin):
    """Вьюсет избранного."""

    relation_field = 'favorites'
    error_exists = 'Данный рецепт уже добавлен'
    error_not_exists = 'Объект уже удален из избранных'

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, pk=None):
        return self.toggle_relation(request, pk)


class CartViewSet(RecipeRelationMixin):
    """Вьюсет корзины."""

    relation_field = 'shopping_cart'
    error_exists = 'Данный рецепт уже добавлен'
    error_not_exists = 'Объект уже удален из списка покупок'

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        return self.toggle_relation(request, pk)


def short_link_redirect(request, code):
    """Редирект по короткой ссылке на рецепт."""

    recipe = get_object_or_404(Recipe, short_code=code)
    return redirect(f'/recipes/{recipe.id}/')
