from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import AvatarSerializer, UserCreateSerializer, UserSerializer


User = get_user_model()


class UserViewSet(UserViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'retrieve'):
            return (AllowAny(),)
        elif self.action == 'list':
            return (IsAdminUser,)
        return super().get_permissions()


class AvatarAPIView(APIView):
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
