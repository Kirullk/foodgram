from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.fields import Base64ImageField
from recipes.serializers import ShortRecipeSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и обновления пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar'
        )
        read_only_fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        request = self.data.get('request')
        return request.user.subscriptions.filter(id=obj.id).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки и обновления аватара пользователя."""
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для списка подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count', 'avatar'
        )

    def get_resipes(self, obj):
        return ShortRecipeSerializer(obj.recipes.all(), many=True)

    def get_recipes_count(self, obj):
        return obj.recipes.count()
