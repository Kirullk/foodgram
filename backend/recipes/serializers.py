from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response

from core.fields import Base64ImageField
from .models import Ingredient, Recipe, RecipeIngredient, Tag
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


class IngredientAmountSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""

    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'ingredients', 'author', 'name',
            'is_in_shopping_cart', 'image', 'text', 'is_favorited',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        return [{'id': ingredient.ingredient.id,
                 'name': ingredient.ingredient.name,
                 'measurement_unit': ingredient.ingredient.measurement_unit,
                 'amount': ingredient.amount}
                for ingredient in obj.recipe_ingredients.all()]

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.favorites.filter(id=obj.id).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.shopping_cart.filter(id=obj.id).exists())


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('id', 'author')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(recipe=recipe, ingredient=i['id'],
                             amount=i['amount'])
            for i in ingredients_data
        ])
        return recipe

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data












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
