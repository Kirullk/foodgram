from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AvatarViewSet, CartViewSet, FavoriteViewSet,
                    IngredientViewSet, RecipeViewSet,
                    SubscribeViewSet, TagViewSet, UserViewSet)


router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'users', AvatarViewSet, basename='avatar')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes', CartViewSet, basename='carts')
router.register(r'recipes', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
    path(
        'users/subscriptions/',
        SubscribeViewSet.as_view({'get': 'subscriptions'}),
        name='subscriptions',
    ),
    path(
        'users/<int:pk>/subscribe/',
        SubscribeViewSet.as_view({'post': 'subscribe', 'delete': 'subscribe'}),
        name='subscribe',
    ),
    path(
        'users/',
        UserViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='user-list',
    ),
    path(
        'users/set_password/',
        UserViewSet.as_view({'post': 'set_password'}),
        name='user-set-password',
    ),
    path(
        'users/me/',
        UserViewSet.as_view({'get': 'me'}),
        name='user-me',
    ),
    path(
        'users/<int:id>/',
        UserViewSet.as_view({'get': 'retrieve'}),
        name='user-detail',
    ),
    path(
        'auth/',
        include('djoser.urls.authtoken')
    ),
]
