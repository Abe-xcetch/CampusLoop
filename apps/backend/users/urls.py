from django.urls import path

from users.views import (
    AuthMeView,
    RegisterView,
    LoginView,
    LogoutView,
    PasswordResetView,
    ProtectedTestView,
)

urlpatterns = [
    path("me/", AuthMeView.as_view(), name="auth-me"),
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("password-reset/", PasswordResetView.as_view(), name="auth-password-reset"),
    path("protected-test/", ProtectedTestView.as_view(), name="auth-protected-test"),
]
