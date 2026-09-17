from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.fields import Base64ImageField
from core.serializers import CreateDeleteSerializer
from recipes.serializers import ShortRecipeSerializer
from users.serializers import UserSerializer


User = get_user_model()


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки и обновления аватара пользователя."""
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class SubscriptionSerializer(CreateDeleteSerializer, UserSerializer):
    """Сериализатор для подписок."""

    object = User
    field = 'subsciptions'
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count', 'avatar'
        )

    def get_recipes(self, obj):
        return ShortRecipeSerializer(obj.recipes.all(), many=True)

    def get_recipes_count(self, obj):
        return obj.recipes.count()
