from django.urls import path, include

# Don't use app_name here - allauth needs its URLs to be in the global namespace
# app_name = 'authentication'  # This would break allauth URL names

urlpatterns = [
    # Include all allauth URLs under /auth/
    # This makes URLs like: /auth/login/, /auth/signup/, etc.
    # But the URL names remain: account_login, account_signup, etc.
    path("", include("allauth.urls")),
    # Future: Custom auth views can be added here with a namespace
    # path('profile/', views.ProfileView.as_view(), name='auth_profile'),
    # path('security/', views.SecuritySettingsView.as_view(), name='auth_security'),
]
