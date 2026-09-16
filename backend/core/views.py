from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class CreateDeleteViewSet(ViewSet):
    url_path = None
    detail = None
    serializer = None

    @action(detail=detail, methods=('post', 'delete'), url_path=url_path)
    def toggle(self, request, pk=None):
        if request.method == 'POST':
            serializer = self.serializer(instance=request.user,
                                         data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            ...