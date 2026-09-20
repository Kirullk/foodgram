from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from core.filters import RecipeFilter
from core.mixins import ListRetrieveMixin
from core.pagination import RecipePagination
from core.permission import IsAuthorOrReadOnly
from core.views import RecipeRelationViewSet
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


class FavoriteViewSet(RecipeRelationViewSet):

    url_path = 'favorite'
    field = 'favorites'


class CartViewSet(RecipeRelationViewSet):

    url_path = 'shopping_cart'
    field = 'shopping_cart'


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch',
                         'delete', 'head', 'options')
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
