from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """Миксин для просмотра нескольких и отдельного объекта."""

    permission_classes = (AllowAny,)


class TagViewSet(ListRetrieveViewSet):
    """Вьюсет для работы с тегами."""

    model = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    """Вьюсет для работы с ингредиентами."""

    model = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
