from django.urls import path

from users.views import AuthMeView

urlpatterns = [
    path("me/", AuthMeView.as_view(), name="auth-me"),
]
