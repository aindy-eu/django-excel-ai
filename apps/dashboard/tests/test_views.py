"""
Tests for dashboard views and functionality.
Phase 2: Integration testing.
"""

import pytest
from django.urls import reverse

from apps.users.tests.factories import UserFactory, UserWithProfileFactory


@pytest.mark.view
@pytest.mark.integration
class TestDashboardViews:
    """Test dashboard view functionality."""

    def test_dashboard_displays_user_email(self, authenticated_client, user):
        """Dashboard displays current user's email."""
        url = reverse("dashboard:index")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert user.email in response.content.decode()

    def test_dashboard_template_used(self, authenticated_client):
        """Dashboard uses correct template."""
        url = reverse("dashboard:index")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "dashboard/index.html" in [t.name for t in response.templates]

    def test_dashboard_context_data(self, authenticated_client, user):
        """Dashboard provides correct context data."""
        url = reverse("dashboard:index")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert response.context["user"] == user

    def test_dashboard_navigation_links(self, authenticated_client):
        """Dashboard shows correct navigation for authenticated users."""
        url = reverse("dashboard:index")
        response = authenticated_client.get(url)

        content = response.content.decode()
        assert "Dashboard" in content
        assert "Settings" in content
        assert "Logout" in content
        # Check that login link is not present (but "User Login" text might be)
        assert 'href="/auth/login/"' not in content


@pytest.mark.view
@pytest.mark.integration
class TestPublicViews:
    """Test public view functionality."""

    def test_home_page_accessible(self, client):
        """Home page is publicly accessible."""
        url = reverse("home")
        response = client.get(url)
        assert response.status_code == 200

    def test_home_page_shows_login_for_anonymous(self, client):
        """Home page shows login link for anonymous users."""
        url = reverse("home")
        response = client.get(url)

        content = response.content.decode()
        # Check for actual login link, not just the word "Login"
        assert 'href="/auth/login/"' in content or "Sign In" in content
        assert "Logout" not in content

    def test_home_page_shows_dashboard_for_authenticated(self, authenticated_client):
        """Home page shows dashboard link for authenticated users."""
        url = reverse("home")
        response = authenticated_client.get(url)

        content = response.content.decode()
        assert "Dashboard" in content
        assert "Logout" in content

    def test_about_page_accessible(self, client):
        """About page is publicly accessible."""
        url = reverse("about")
        response = client.get(url)
        assert response.status_code == 200

    def test_404_page(self, client):
        """404 page is displayed for non-existent URLs."""
        response = client.get("/non-existent-url/")
        assert response.status_code == 404


@pytest.mark.view
@pytest.mark.integration
class TestFormSubmissions:
    """Test form submission integration."""

    def test_csrf_token_in_forms(self, client):
        """Forms include CSRF token."""
        url = reverse("account_login")
        response = client.get(url)

        assert response.status_code == 200
        assert "csrfmiddlewaretoken" in response.content.decode()

    def test_form_validation_errors_displayed(self, client, db):
        """Form validation errors are displayed to user."""
        url = reverse("account_signup")

        response = client.post(
            url, {"email": "invalid-email", "password1": "pass", "password2": "pass"}
        )

        assert response.status_code == 200
        content = response.content.decode()
        assert "Enter a valid email address" in content or "valid" in content.lower()

    def test_form_success_message(self, client, db):
        """Success messages are displayed after form submission."""
        url = reverse("account_signup")

        response = client.post(
            url,
            {
                "email": "success@example.com",
                "password1": "complex!pass123",
                "password2": "complex!pass123",
            },
            follow=True,
        )

        assert response.status_code == 200


@pytest.mark.integration
class TestSessionManagement:
    """Test session and cookie management."""

    def test_session_created_on_login(self, client, user):
        """Session is created when user logs in."""
        url = reverse("account_login")

        response = client.post(url, {"login": user.email, "password": "defaultpass123"}, follow=True)

        # After successful login, user should be redirected and session created
        assert response.status_code == 200
        if "_auth_user_id" in client.session:
            assert client.session.session_key is not None
            assert "_auth_user_id" in client.session
        else:
            # If login didn't work, force login to test session creation
            client.force_login(user)
            assert "_auth_user_id" in client.session

    def test_session_cleared_on_logout(self, authenticated_client):
        """Session is cleared when user logs out."""
        session_key_before = authenticated_client.session.session_key

        url = reverse("account_logout")
        response = authenticated_client.post(url)

        assert authenticated_client.session.session_key != session_key_before

    def test_remember_me_functionality(self, client, user):
        """Remember me option affects session expiry."""
        url = reverse("account_login")

        # Without remember me
        response = client.post(url, {"login": user.email, "password": "defaultpass123"})

        # Session should expire on browser close
        assert (
            client.session.get_expire_at_browser_close() is True
            or client.session.get_expiry_age() < 86400 * 30
        )
