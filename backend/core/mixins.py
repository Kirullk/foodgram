from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny


class ListRetrieveMixin(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Миксин для просмотра нескольких и отдельного объекта."""

    permission_classes = (AllowAny,)
