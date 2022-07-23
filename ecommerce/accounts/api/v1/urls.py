from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    GetTOTPRequestIDView,
    LoginView,
    ProfileRetrieveUpdateView,
    RegisterView,
    ValidateTOTPView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path(
        "profile/<int:pk>/",
        ProfileRetrieveUpdateView.as_view(),
        name="user_profile",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("totp/get-request-id/", GetTOTPRequestIDView.as_view()),
    path("totp/validate/", ValidateTOTPView.as_view()),
]
