from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status

from .serializers import AvatarSerializer, SubscriptionSerializer, UserCreateSerializer, UserSerializer
from core.pagination import UserPagination


User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователями."""

    pagination_class = UserPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


class AvatarViewSet(APIView):
    """Вьюха для работы с аватаром текущего пользователя."""

    def post(self, request):
        serializer = AvatarSerializer(instance=request.user,
                                      data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionAPIView(APIView):

    def get(self, request):
        subscriptions = request.user.subscriptions.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
