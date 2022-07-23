from django.urls import path, re_path

from .views import (
    AccountSettingsView,
    CustomPasswordChangeView,
    EditUserProfileView,
    UserProfileView,
    UserRegisterationView,
    password_change_success,
)

urlpatterns = [
    path("register/", UserRegisterationView.as_view(), name="register"),
    path("account-settings/", AccountSettingsView.as_view(), name="account_settings"),
    path("password/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("password-success/", password_change_success, name="password_success"),
    re_path("(?P<slug>[-\w]+)/profile/", UserProfileView.as_view(), name="profile"),
    re_path(
        "(?P<slug>[-\w]+)/edit-profile/",
        EditUserProfileView.as_view(),
        name="edit_profile",
    ),
]
