from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from recipes.serializers import ShortRecipeSerializer


class RecipeRelationViewSet(GenericViewSet):
    url_path = None
    field = None
    serializer_class = ShortRecipeSerializer

    @action(detail=True, methods=('post', 'delete'))
    def toggle(self, request, pk=None):
        url_path = self.url_path
        if request.method == 'POST':
            serializer = self.get_serializer(
                data=request.data,
                context={'request': request, 'pk': pk, 'field': self.field},
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            fields = getattr(request.user, self.field)
            obj = get_object_or_404(self.object, pk=pk)
            if fields.filter(id=obj.id).exists():
                fields.remove(obj)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Данная запись не существует'},
                            status=status.HTTP_400_BAD_REQUEST)
