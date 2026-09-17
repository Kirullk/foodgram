from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AvatarSerializer, SubscriptionSerializer
from core.views import CreateDeleteViewSet


User = get_user_model()


class AvatarViewSet(CreateDeleteViewSet):
    """Вьюха для работы с аватаром текущего пользователя."""

    serializer = AvatarSerializer
    object = User
    field = 'avatar'


class SubscriptionAPIView(APIView):

    def get(self, request):
        subscriptions = request.user.subscriptions.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeViewSet(CreateDeleteViewSet):

    detail = True
    url_path = 'subscribe'
    serializer = SubscriptionSerializer
    object = User
    field = 'subscriptions'
