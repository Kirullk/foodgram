from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """Миксин для просмотра нескольких и отдельного объекта."""

    permission_classes = (AllowAny,)


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """Миксин для просмотра создания и удаления объекта."""

    pass
