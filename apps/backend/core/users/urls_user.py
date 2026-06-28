from django.urls import path
from core.users.presentation.views import UserMeView, PublicUserProfileView

urlpatterns = [
    path("me", UserMeView.as_view(), name="user-me"),
    path("<str:pk>/profile", PublicUserProfileView.as_view(), name="user-profile"),
]
