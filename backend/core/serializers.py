from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class CreateDeleteSerializer:
    field = None
    object = None

    def create(self, validated_data):
        pk = self.context.get('pk')
        fields = getattr(self.instance, self.field)
        if pk:
            obj = get_object_or_404(self.object, pk=pk)
            if not fields.filter(id=obj.id).exists():
                fields.add(obj)
                return self.object
            return Response({'error': 'Данная запись уже добавлена'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().create(validated_data)

    def delete(self):
        fields = getattr(self.instance, self.field)
        if self.context.get('detail'):
            obj = get_object_or_404(self.object, pk=self.context.get('pk'))
            if fields.filter(id=obj.id).exists():
                fields.remove(obj)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Данная запись не существует'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            fields.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
