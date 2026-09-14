from django.urls import path

from .views import AvatarAPIView, UserViewSet


urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'})),
    path('', UserViewSet.as_view({'post': 'create'})),
    path('<int:id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('me/', UserViewSet.as_view({'get': 'me'})),
    path('me/avatar/', AvatarAPIView.as_view())
]
