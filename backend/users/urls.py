from django.urls import path, include

from .views import UserViewSet


urlpatterns = [
    path(
        '',
        UserViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='user-list',
    ),
    path(
        '<int:id>/',
        UserViewSet.as_view({'get': 'retrieve'}),
        name='user-detail',
    ),
    path(
        'set_password/',
        UserViewSet.as_view({'post': 'set_password'}),
        name='user-set-password',
    ),
    path(
        '',
        include('djoser.urls.authtoken')
    ),
]
