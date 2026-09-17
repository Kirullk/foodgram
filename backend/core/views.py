from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class CreateDeleteViewSet(ViewSet):
    detail = False
    url_path = None
    serializer = None
    status = status.HTTP_201_CREATED if detail else status.HTTP_200_OK

    @action(detail=detail, methods=('post', 'delete'), url_path=url_path)
    def toggle(self, request, pk=None):

        serializer = self.serializer(instance=request.user,
                                     data=request.data,
                                     context={'request': request,
                                              'pk': pk,
                                              'detail': self.detail})
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save()
                return Response(serializer.data, status=self.status)

            elif request.method == 'DELETE':
                return serializer.delete()
