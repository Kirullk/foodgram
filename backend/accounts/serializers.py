from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.fields import Base64ImageField
from recipes.serializers import ShortRecipeSerializer
from users.serializers import UserSerializer


User = get_user_model()


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки и обновления аватара пользователя."""
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count', 'avatar'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        limit = request.query_params.get('recipes_limit')
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
