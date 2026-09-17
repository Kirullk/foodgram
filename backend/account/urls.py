from django.urls import path, include
from rest_framework.routers import DefaultRouters

from .views import AvatarViewSet, SubscribeViewSet, SubscriptionAPIView, UserViewSet


router = DefaultRouters()
router.register('', SubscribeViewSet, basename='subscribe')


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
        AvatarViewSet.as_view(),
        name='user-avatar',
    ),
    path(
        'subscriptions/',
        SubscriptionAPIView.as_view(),
        name='subscriptions-list'
    ),
]
