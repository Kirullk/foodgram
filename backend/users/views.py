from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status

from .serializers import AvatarSerializer, SubscriptionSerializer, UserCreateSerializer, UserSerializer
from core.pagination import UserPagination
from core.views import CreateDeleteViewSet


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователями."""

    pagination_class = UserPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


class AvatarViewSet(CreateDeleteViewSet):
    """Вьюха для работы с аватаром текущего пользователя."""

    serializer = AvatarSerializer


class SubscriptionAPIView(APIView):

    def get(self, request):
        subscriptions = request.user.subscriptions.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscibeViewSet(CreateDeleteViewSet):

    detail = True
    url_path = 'subscribe'
    serializer = SubscriptionSerializer
