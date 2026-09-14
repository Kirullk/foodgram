import base64
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('base:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)



class UserSerializer(serializers.ModelSerializer):
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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        read_only_fields = ('id')
        extra_kwargs = {'password': {'write_only': True}}


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)
