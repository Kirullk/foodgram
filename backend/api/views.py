from io import BytesIO

from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef, Sum
from django.http import FileResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
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
from recipes.models import (Favorite, Ingredient,
                            Recipe, RecipeIngredient, ShoppingCart, Tag)
from users.models import Follow
from .serializers import (AvatarSerializer, FavoriteCreateSerializer,
                          IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShoppingCartCreateSerializer,
                          SubscriptionWriteSerializer,
                          SubscriptionReadSerializer, TagSerializer,
                          UserSerializer)


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет пользователей."""

    pagination_class = Pagination

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Возвращает данные текущего пользователя."""

        serializer = UserSerializer(
            request.user,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        """Подписка на пользователя."""
        author = get_object_or_404(User, id=id)
        serializer = SubscriptionWriteSerializer(
            data={'user': request.user.id,
                  'author': author.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        """Отписка от пользователя."""
        author = get_object_or_404(User, id=id)
        deleted, _ = Follow.objects.filter(
            user=request.user, author=author
        ).delete()

        if not deleted:
            return Response(
                {'error': 'Вы не подписаны на данного пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=('put',),
            url_path='me/avatar',
            permission_classes=(IsAuthenticated,),)
    def update_avatar(self, request):
        serializer = AvatarSerializer(
            instance=request.user,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @update_avatar.mapping.delete
    def delete_avatar(self, request):
        request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=('get',),
            url_path='subscriptions',
            permission_classes=(IsAuthenticated,),)
    def subscriptions(self, request):
        authors = User.objects.filter(
            subscriptions_to_author__user=request.user
        ).annotate(
            recipes_count=Count('recipes')
        ).order_by('username')
        page = self.paginate_queryset(authors)
        serializer = SubscriptionReadSerializer(
            page, many=True, context={'request': request},
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""

    queryset = Recipe.objects.select_related('author').prefetch_related(
        'tags',
        'recipe_ingredients__ingredient',
    )
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_queryset(self):
        """Queryset с аннотациями избранного и корзины."""
        queryset = super().get_queryset()
        user = self.request.user
        is_favorited = False
        is_in_shopping_cart = False

        if user.is_authenticated:
            is_favorited = Exists(
                Favorite.objects.filter(
                    user=user, recipe=OuterRef('pk')
                )
            )
            is_in_shopping_cart = Exists(
                ShoppingCart.objects.filter(
                    user=user, recipe=OuterRef('pk')
                )
            )

        return queryset.annotate(
            is_favorited=is_favorited,
            is_in_shopping_cart=is_in_shopping_cart
        ).order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def format_shopping_cart(ingredients):
        """Формирует текст списка покупок."""
        lines = ['Список покупок:', '']
        for item in ingredients:
            lines.append(
                f'{item["ingredient__name"]} — '
                f'{item["total_amount"]} '
                f'({item["ingredient__measurement_unit"]})'
            )
        return '\n'.join(lines)

    @staticmethod
    def add_to(serializer_class, request, pk):
        """Добавляет рецепт."""
        get_object_or_404(Recipe, pk=pk)

        serializer = serializer_class(
            data={'user': request.user.id, 'recipe': pk},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def remove_from(model, request, pk):
        """Удаляет рецепт."""
        get_object_or_404(Recipe, pk=pk)

        deleted, _ = model.objects.filter(
            user=request.user, recipe_id=pk
        ).delete()
        if not deleted:
            return Response(
                {'error': 'Рецепта нет в этом списке.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post',)
    )
    def favorite(self, request, pk=None):
        """Добавить рецепт в избранное."""
        return self.add_to(FavoriteCreateSerializer, request, pk)

    @favorite.mapping.delete
    def unfavorite(self, request, pk=None):
        """Удалить рецепт из избранного."""
        return self.remove_from(Favorite, request, pk)

    @action(
        detail=True,
        methods=('post',),
    )
    def shopping_cart(self, request, pk=None):
        """Добавить рецепт в список покупок."""
        return self.add_to(ShoppingCartCreateSerializer, request, pk)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        """Удалить рецепт из списка покупок."""
        return self.remove_from(ShoppingCart, request, pk)

    @action(detail=True, methods=('get',), url_path='get-link',
            permission_classes=(AllowAny,),)
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_link = request.build_absolute_uri(
            reverse('short-link', args=[recipe.short_code])
        )
        return Response(
            {'short-link': short_link},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=('get',)
    )
    def download_shopping_cart(self, request):
        """Скачивает список покупок пользователя."""
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(
            total_amount=Sum('amount'),
        ).order_by('ingredient__name')

        content = self.format_shopping_cart(ingredients)
        buffer = BytesIO(content.encode('utf-8'))

        return FileResponse(
            buffer,
            as_attachment=True,
            filename='shopping_cart.txt',
            content_type='text/plain; charset=utf-8',
        )


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
    try:
        recipe = Recipe.objects.get(short_code=code)
        url = f'/recipes/{recipe.id}/'
    except Recipe.DoesNotExist:
        url = '/not_found'

    return HttpResponsePermanentRedirect(
        request.build_absolute_uri(url)
    )
