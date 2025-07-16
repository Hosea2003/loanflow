from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import ListUserView, RegisterUserView, UserDetailsView

urlpatterns=[
    path("register/", RegisterUserView.as_view(), name='register'),
    path('get-token/', TokenObtainPairView.as_view(), name='get-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('details/<int:id>', UserDetailsView.as_view(), name='details-user'),
    path('list', ListUserView.as_view(), name='list-users')
]