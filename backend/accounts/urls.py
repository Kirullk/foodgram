from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AvatarViewSet, SubscribeViewSet
from users.views import UserViewSet


router = DefaultRouter()
router.register('', AvatarViewSet, basename='avatar')
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
    )
]
