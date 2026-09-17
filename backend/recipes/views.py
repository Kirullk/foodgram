from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets


from core import mixins
from core.views import CreateDeleteViewSet
from .models import Ingredient, Recipe, Tag
from .paginator import RecipePagination
from .serializers import IngredientSerializer, RecipeSerializer, ShortRecipeSerializer, TagSerializer


class TagViewSet(mixins.ListRetrieveViewSet):
    """Вьюсет для работы с тегами."""

    model = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(mixins.ListRetrieveViewSet):
    """Вьюсет для работы с ингредиентами."""

    model = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class FavoriteViewSet(CreateDeleteViewSet):

    detail = True
    url_path = 'favorite'
    serializer = ShortRecipeSerializer
    object = Recipe
    field = 'favorites'


class CartViewSet(CreateDeleteViewSet):

    detail = True
    url_path = 'shopping_cart'
    serializer = ShortRecipeSerializer
    object = Recipe
    field = 'shopping_cart'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ('get', 'post', 'patch',
                         'delete', 'head', 'options')
    paginaton_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('user__id', 'tag__slug')

    def permission_classes(self):
        if self.action in ('patch', 'delete'):
            return IsAuthor
        return super().permission_classes()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
