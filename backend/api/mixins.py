from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import ShortRecipeSerializer


class ListRetrieveMixin(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Миксин для просмотра нескольких и отдельного объекта."""

    permission_classes = (AllowAny,)


class RecipeRelationMixin(viewsets.GenericViewSet):
    """Миксин для добавления/удаления рецепта в связи пользователя."""

    relation_field = None
    error_exists = 'Уже добавлено'
    error_not_exists = 'Не добавлено'

    def toggle_relation(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = getattr(request.user, self.relation_field)

        if request.method == 'POST':
            if relation.filter(id=recipe.id).exists():
                return Response(
                    {'error': self.error_exists},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            relation.add(recipe)
            return Response(
                ShortRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED,
            )

        if not relation.filter(id=recipe.id).exists():
            return Response(
                {'error': self.error_not_exists},
                status=status.HTTP_400_BAD_REQUEST,
            )
        relation.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)
