from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserSerializer as DjoserUserSerializer,
    UserCreateSerializer as DjoserUserCreateSerializer,
)
User = get_user_model()


class UserSerializer(DjoserUserSerializer):
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
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return request.user.subscriptions.filter(id=obj.id).exists()


class UserCreateSerializer(DjoserUserCreateSerializer):
    """Сериализатор для регистрации нового пользователя."""

    first_name = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=150,
    )
    last_name = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=150,
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}
