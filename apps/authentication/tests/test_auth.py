"""
Tests for authentication flow with Django Allauth.
Phase 1: Core authentication testing.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.users.tests.factories import UserFactory

User = get_user_model()


@pytest.mark.auth
@pytest.mark.integration
class TestLoginFlow:
    """Test email-based login flow."""

    def test_login_url_accessible(self, client):
        """Login page is accessible."""
        url = reverse("account_login")
        response = client.get(url)
        assert response.status_code == 200

    def test_login_with_email(self, client, db):
        """User can login with email and password."""
        user = UserFactory(email="login@example.com", password="testpass123")
        url = reverse("account_login")

        response = client.post(
            url, {"login": "login@example.com", "password": "testpass123"}
        )

        assert response.status_code == 302
        assert response.url == "/dashboard/"

    def test_login_with_wrong_password(self, client, db):
        """Login fails with wrong password."""
        user = UserFactory(email="wrong@example.com", password="correct123")
        url = reverse("account_login")

        response = client.post(
            url, {"login": "wrong@example.com", "password": "wrong123"}
        )

        assert response.status_code == 200
        assert (
            "The email address and/or password you specified are not correct"
            in response.content.decode()
        )

    def test_login_with_nonexistent_email(self, client, db):
        """Login fails with nonexistent email."""
        url = reverse("account_login")

        response = client.post(
            url, {"login": "nonexistent@example.com", "password": "anypass123"}
        )

        assert response.status_code == 200
        assert (
            "The email address and/or password you specified are not correct"
            in response.content.decode()
        )

    def test_login_inactive_user(self, client, db):
        """Inactive users are redirected to inactive page."""
        user = UserFactory(
            email="inactive@example.com", password="testpass123", is_active=False
        )
        url = reverse("account_login")

        response = client.post(
            url, {"login": "inactive@example.com", "password": "testpass123"}
        )

        # Allauth redirects inactive users to a special page
        assert response.status_code == 302
        assert "/auth/inactive/" in response.url

    def test_login_redirect_next_parameter(self, client, db):
        """Login redirects to 'next' parameter after success."""
        user = UserFactory(email="redirect@example.com", password="testpass123")
        url = reverse("account_login")

        response = client.post(
            f"{url}?next=/dashboard/profile/",
            {"login": "redirect@example.com", "password": "testpass123"},
        )

        assert response.status_code == 302
        assert response.url == "/dashboard/profile/"

    def test_authenticated_user_redirect(self, authenticated_client):
        """Already authenticated users are redirected from login."""
        url = reverse("account_login")
        response = authenticated_client.get(url)
        assert response.status_code == 302


@pytest.mark.auth
@pytest.mark.integration
class TestLogoutFlow:
    """Test logout functionality."""

    def test_logout_url_requires_login(self, client):
        """Logout URL redirects anonymous users to home."""
        url = reverse("account_logout")
        response = client.get(url)
        assert response.status_code == 302
        # Allauth redirects to home when anonymous users try to logout
        assert response.url == "/"

    def test_logout_success(self, authenticated_client):
        """Authenticated user can logout."""
        url = reverse("account_logout")
        response = authenticated_client.post(url)
        assert response.status_code == 302
        assert response.url == "/"

    def test_logout_clears_session(self, client, user):
        """Logout clears user session."""
        client.force_login(user)
        assert "_auth_user_id" in client.session

        url = reverse("account_logout")
        response = client.post(url)

        assert "_auth_user_id" not in client.session


@pytest.mark.auth
@pytest.mark.integration
class TestSignupFlow:
    """Test user registration flow."""

    def test_signup_url_accessible(self, client):
        """Signup page is accessible."""
        url = reverse("account_signup")
        response = client.get(url)
        assert response.status_code == 200

    def test_signup_with_email(self, client, db):
        """User can signup with email."""
        url = reverse("account_signup")

        response = client.post(
            url,
            {
                "email": "newuser@example.com",
                "password1": "complex!pass123",
                "password2": "complex!pass123",
            },
        )

        assert response.status_code == 302
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_signup_duplicate_email(self, client, db):
        """Signup fails with duplicate email."""
        UserFactory(email="existing@example.com")
        url = reverse("account_signup")

        response = client.post(
            url,
            {
                "email": "existing@example.com",
                "password1": "complex!pass123",
                "password2": "complex!pass123",
            },
        )

        assert response.status_code == 200
        assert (
            "A user is already registered with this email address"
            in response.content.decode()
        )

    def test_signup_password_mismatch(self, client, db):
        """Signup fails when passwords don't match."""
        url = reverse("account_signup")

        response = client.post(
            url,
            {
                "email": "mismatch@example.com",
                "password1": "complex!pass123",
                "password2": "different!pass123",
            },
        )

        assert response.status_code == 200
        assert not User.objects.filter(email="mismatch@example.com").exists()

    def test_signup_weak_password(self, client, db):
        """Signup fails with weak password."""
        url = reverse("account_signup")

        response = client.post(
            url, {"email": "weak@example.com", "password1": "123", "password2": "123"}
        )

        assert response.status_code == 200
        assert not User.objects.filter(email="weak@example.com").exists()


@pytest.mark.auth
@pytest.mark.integration
class TestProtectedViews:
    """Test login required functionality."""

    def test_dashboard_requires_login(self, client):
        """Dashboard requires authentication."""
        url = reverse("dashboard:index")
        response = client.get(url)
        assert response.status_code == 302
        assert "/auth/login/" in response.url

    def test_dashboard_accessible_when_authenticated(self, authenticated_client):
        """Dashboard is accessible for authenticated users."""
        url = reverse("dashboard:index")
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_profile_requires_login(self, client):
        """Profile page requires authentication."""
        url = reverse("users:profile")
        response = client.get(url)
        assert response.status_code == 302
        assert "/auth/login/" in response.url

    def test_profile_accessible_when_authenticated(self, authenticated_client):
        """Profile is accessible for authenticated users."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_admin_disabled_in_test_mode(self, client, user, admin_user):
        """Admin returns 404 in test mode (DEBUG=False by default)."""
        url = "/admin/"

        # All users get 404 when admin is disabled
        response = client.get(url)
        assert response.status_code == 404

        # Even admin users get 404
        client.force_login(admin_user)
        response = client.get(url)
        assert response.status_code == 404
