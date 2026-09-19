from django.urls import include, path
from rest_framework import routers

from .views import (CartViewSet, FavoriteViewSet, IngredientViewSet,
                    RecipeViewSet, TagViewSet)


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes', CartViewSet, basename='carts')
router.register(r'recipes', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls))
]
