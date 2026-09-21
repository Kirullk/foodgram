from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet

from core.pagination import UserPagination


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователями."""

    pagination_class = UserPagination
