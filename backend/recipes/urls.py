from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, TagViewSet


router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls))
]
