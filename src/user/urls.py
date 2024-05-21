from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import (
    UserCreateView,
    UserLoginView,
    UserLogoutView,
    UserChangePasswordView,
    UserForgotPasswordView,
    ProfileCreateAPIView,
    ProfileUpdateAPIView,
)

urlpatterns = [
    path("create", UserCreateView.as_view()),
    path("login", UserLoginView.as_view()),
    path("logout", UserLogoutView.as_view()),
    path("change-password", UserChangePasswordView.as_view()),
    path("forgot", UserForgotPasswordView.as_view()),
    path("profile/create", ProfileCreateAPIView.as_view(), name="profile-create"),
    path("profile/update", ProfileUpdateAPIView.as_view(), name="profile-update"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
