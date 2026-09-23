from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AvatarViewSet, CartViewSet, FavoriteViewSet,
                    IngredientViewSet, RecipeViewSet, SubscribeViewSet,
                    TagViewSet, UserViewSet)


router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes', CartViewSet, basename='carts')
router.register(r'recipes', FavoriteViewSet, basename='favorites')
router.register('', AvatarViewSet, basename='avatar')
router.register('', SubscribeViewSet, basename='subscriptions')

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),
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
        'set_password/',
        UserViewSet.as_view({'post': 'set_password'}),
        name='user-set-password',
    ),
    path(
        'me/',
        UserViewSet.as_view({'get': 'me'}),
        name='user-me',
    ),
    path(
        '',
        include('djoser.urls.authtoken')
    ),
]
