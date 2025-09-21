from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
    path(
        "profile/emails/", views.EmailManagementView.as_view(), name="email_management"
    ),
    path("profile/avatar/", views.AvatarUploadView.as_view(), name="avatar_upload"),
]
