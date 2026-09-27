from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from api.constants import (MAX_AMOUNT, MIN_AMOUNT,
                           MAX_COOKING_TIME, MIN_COOKING_TIME)
from recipes.models import (Favorite, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
from users.models import Follow


User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    """Сериализатор пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = DjoserUserSerializer.Meta.fields + (
            'is_subscribed', 'avatar',
        )
        read_only_fields = (
            DjoserUserSerializer.Meta.read_only_fields
            + ('is_subscribed', 'avatar')
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request
                and request.user.is_authenticated
                and obj.subscribers.filter(user=request.user).exists())


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара пользователя."""

    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class SubscriptionSerializer(UserSerializer):
    """Сериализатор подписок с рецептами автора."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        if request:
            limit = request.query_params.get('recipes_limit')
            try:
                recipes = recipes[:int(limit)]
            except (TypeError, ValueError):
                pass
        return ShortRecipeSerializer(
            recipes, many=True, context=self.context
        ).data


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор создания подписки."""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, attrs):
        user = attrs['user']
        author = attrs['author']

        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя.'
            )
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        return attrs

    def to_representation(self, instance):
            author = User.objects.filter(
                pk=instance.author_id
            ).annotate(
                recipes_count=Count('recipes')
            ).first()
            return SubscriptionSerializer(
                author, context=self.context,
            ).data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.Serializer):
    """Сериализатор ингредиента с количеством."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        error_messages={
            'does_not_exist': 'Ингредиент с таким id не найден.',
            'incorrect_type': 'id должен быть числом.',
        },
    )
    amount = serializers.IntegerField(
        min_value=MIN_AMOUNT,
        max_value=MAX_AMOUNT,
        error_messages={
            'min_value': f'Количество не может быть меньше {MIN_AMOUNT}.',
            'max_value': f'Количество не может быть больше {MAX_AMOUNT}.',
        },
    )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента в рецепте (для чтения)."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для чтения."""

    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True
    )
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
        return [
            {
                'id': ingredient.ingredient.id,
                'name': ingredient.ingredient.name,
                'measurement_unit': ingredient.ingredient.measurement_unit,
                'amount': ingredient.amount,
            }
            for ingredient in obj.recipe_ingredients.all()
        ]

    def get_is_favorited(self, obj):
        request = self.context['request']
        return (request
                and request.user.is_authenticated
                and obj.favorites.filter(user=request.user).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        return (request
                and request.user.is_authenticated
                and obj.shopping_cart.filter(user=request.user).exists())


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления рецепта."""

    ingredients = IngredientAmountSerializer(many=True, required=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=True,
    )
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME,
        error_messages={
            'min_value': (
                f'Время приготовления не может быть меньше {MIN_COOKING_TIME}.'
            ),
            'max_value': (
                f'Время приготовления не может быть больше {MAX_COOKING_TIME}.'
            ),
        },
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('id', 'author')

    @staticmethod
    def create_recipe_ingredients(recipe, ingredients_data):
        """Создаёт ингредиенты для рецепта одним запросом."""

        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients_data
        ])

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Список ингредиентов не может быть пустым.'
            )
        ingredient_ids = [ingredient['id'].id for ingredient in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться.'
            )
        return ingredients

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                'Список тегов не может быть пустым.'
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                'Теги не должны повторяться.'
            )
        return tags

    def validate_image(self, image):
        if not image:
            raise serializers.ValidationError(
                'Поле image обязательно.'
            )
        return image

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.create_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        tags_data = validated_data.pop('tags', None)

        if ingredients_data is None:
            raise serializers.ValidationError(
                {'ingredients': 'Обязательное поле.'}
            )
        if tags_data is None:
            raise serializers.ValidationError(
                {'tags': 'Обязательное поле.'}
            )

        instance = super().update(instance, validated_data)
        instance.tags.set(tags_data)
        instance.recipe_ingredients.all().delete()
        self.create_recipe_ingredients(instance, ingredients_data)
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта (кратко)."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AbstractUserRecipeSerializer(serializers.ModelSerializer):
    """Абстрактный сериализатор связи пользователя и рецепта."""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        fields = ('user', 'recipe')

    def validate(self, attrs):
        user = attrs['user']
        recipe = attrs['recipe']
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                self.error_message
            )
        return attrs

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe,
            context=self.context,
        ).data


class FavoriteCreateSerializer(AbstractUserRecipeSerializer):
    """Сериализатор создания избранного."""

    error_message = 'Рецепт уже добавлен в избранное.'

    class Meta(AbstractUserRecipeSerializer.Meta):
        model = Favorite


class ShoppingCartCreateSerializer(AbstractUserRecipeSerializer):
    """Сериализатор создания списка покупок."""

    error_message = 'Рецепт уже добавлен в список покупок.'

    class Meta(AbstractUserRecipeSerializer.Meta):
        model = ShoppingCart
