from django.urls import path, include

from .views import AvatarAPIView, UserViewSet


urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('me/avatar/', AvatarAPIView.as_view()),
    path('set_password/', UserViewSet({'post': 'set_password'})),
    path('', include('djoser.urls.authtoken')),
]
