from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AvatarViewSet, SubscribeViewSet, SubscriptionAPIView
from users.views import UserViewSet


router = DefaultRouter()
router.register('', SubscribeViewSet, basename='subscriptions')


urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
    path(
        'me/',
        UserViewSet.as_view({'get': 'me'}),
        name='user-me',
    ),
    path(
        'me/avatar/',
        AvatarViewSet.as_view({'post': 'action', 'delete': 'action'}),
        name='user-avatar',
    ),
    path(
        'subscriptions/',
        SubscriptionAPIView.as_view(),
        name='subscriptions-list'
    ),
]
