from django.urls import include, path
from rest_framework import routers

from .views import CartViewSet, FavoriteViewSet, IngredientViewSet, TagViewSet


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register('', CartViewSet, basename='cart')
router.register('', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls))
]
