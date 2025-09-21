from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.urls import reverse


class AuthenticationAdapter(DefaultAccountAdapter):
    """Custom adapter for allauth to control authentication behavior."""

    def get_login_redirect_url(self, request):
        """Redirect to dashboard after successful login."""
        return getattr(settings, "LOGIN_REDIRECT_URL", "/dashboard/")

    def get_logout_redirect_url(self, request):
        """Redirect to home after logout."""
        return getattr(settings, "LOGOUT_REDIRECT_URL", "/")

    def is_open_for_signup(self, request):
        """Control whether signups are allowed."""
        return getattr(settings, "ACCOUNT_ALLOW_SIGNUP", True)

    def save_user(self, request, user, form, commit=True):
        """Hook to customize user saving (e.g., for audit logging)."""
        user = super().save_user(request, user, form, commit=False)

        # Future: Add audit logging here
        # from libs.audit import log_user_creation
        # log_user_creation(user, request)

        if commit:
            user.save()
        return user
