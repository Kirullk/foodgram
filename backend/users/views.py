from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet

from core.pagination import UserPagination
from .serializers import UserCreateSerializer, UserSerializer


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователями."""

    pagination_class = UserPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
