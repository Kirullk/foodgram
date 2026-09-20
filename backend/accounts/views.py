from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import AvatarSerializer, SubscriptionSerializer
from core.pagination import UserPagination


User = get_user_model()


class AvatarViewSet(GenericViewSet):

    @action(detail=False, methods=('put', 'delete'), url_path='me/avatar')
    def avatar(self, request):
        if request.method == 'PUT':
            serializer = AvatarSerializer(
                instance=request.user,
                data=request.data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeViewSet(GenericViewSet):
    pagination_class = UserPagination

    @action(detail=False, methods=('get',), url_path='subscriptions')
    def subscriptions(self, request):
        subs = request.user.subscriptions.all()
        page = self.paginate_queryset(subs)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=('post', 'delete'))
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        subscriptions = request.user.subscriptions

        if request.method == 'POST':
            if author == request.user:
                return Response({'error': 'Нельзя подписаться на себя'},
                                status=status.HTTP_400_BAD_REQUEST)
            if subscriptions.filter(id=author.id).exists():
                return Response({'error': 'Вы уже подписаны'},
                                status=status.HTTP_400_BAD_REQUEST)
            subscriptions.add(author)
            serializer = SubscriptionSerializer(author,
                                                context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not subscriptions.filter(id=author.id).exists():
            return Response({'error': 'Вы не подписаны'},
                            status=status.HTTP_400_BAD_REQUEST)
        subscriptions.remove(author)
        return Response(status=status.HTTP_204_NO_CONTENT)
