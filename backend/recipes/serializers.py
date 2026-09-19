from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response

from core.fields import Base64ImageField
from .models import Ingredient, Recipe, Tag
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(IngredientSerializer):
    amount = serializers.IntegerField(min_value=1)

    class Meta(IngredientSerializer.Meta):
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов со полным перечнем полей."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    tags = TagSerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = (
            'id', 'author', 'is_favorited', 'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.favorites.filter(id=obj.id).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.shopping_cart.filter(id=obj.id).exists())


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def create(self):
        fields = getattr(self.context.get('request').user,
                         self.context.get('field'))
        obj = get_object_or_404(Recipe, pk=self.context.get('pk'))
        if fields.filter(id=obj.id).exists():
            return Response({'error': 'Данная запись уже добавлена'},
                            status=status.HTTP_400_BAD_REQUEST)
        fields.add(obj)
        return self.object
