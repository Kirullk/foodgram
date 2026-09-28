from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Расширенная админка пользователя."""

    list_display = ('id', 'email', 'username', 'first_name',
                    'last_name', 'recipes_count', 'subscribers_count')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    @admin.display(description='Рецептов')
    def recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Подписчиков')
    def subscribers_count(self, obj):
        return obj.authors_subscribers.count()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админка подписок."""

    list_display = ('id', 'user', 'author')
    search_fields = ('user__username', 'author__username')
    list_filter = ('user', 'author')
