from django.urls import path, include
from rest_framework import routers

from .views import AvatarViewSet, SubscriptionAPIView, UserViewSet


urlpatterns = [
    path(
        '',
        UserViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='user-list',
    ),
    path(
        '<int:id>/',
        UserViewSet.as_view({'get': 'retrieve'}),
        name='user-detail',
    ),
    path(
        'me/',
        UserViewSet.as_view({'get': 'me'}),
        name='user-me',
    ),
    path(
        'me/avatar/',
        AvatarViewSet.as_view(),
        name='user-avatar',
    ),
    path(
        'set_password/',
        UserViewSet.as_view({'post': 'set_password'}),
        name='user-set-password',
    ),
    path(
        '',
        include('djoser.urls.authtoken')
    ),
    path(
        'subscriptions/',
        SubscriptionAPIView.as_view(),
        name='subscriptions-list'
    ),
]
