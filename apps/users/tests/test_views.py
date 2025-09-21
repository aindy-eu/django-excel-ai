"""
Tests for user views including profile functionality.
"""

import pytest
from django.urls import reverse

from apps.users.tests.factories import UserFactory, UserWithProfileFactory


@pytest.mark.view
@pytest.mark.integration
class TestProfileViews:
    """Test profile view functionality."""

    def test_profile_url_accessible(self, authenticated_client):
        """Profile page is accessible for authenticated users."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_profile_requires_login(self, client):
        """Profile page requires authentication."""
        url = reverse("users:profile")
        response = client.get(url)
        assert response.status_code == 302
        assert "/auth/login/" in response.url

    def test_profile_template_used(self, authenticated_client):
        """Profile page uses correct template."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert "users/profile.html" in [t.name for t in response.templates]

    def test_profile_context_data(self, authenticated_client, user):
        """Profile page provides correct context data."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.context["user"] == user

    def test_profile_displays_user_info(self, authenticated_client, user):
        """Profile displays user information."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        content = response.content.decode()
        assert user.email in content

    def test_profile_email_management_link(self, authenticated_client):
        """Profile shows email management functionality."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        content = response.content.decode()
        assert "Manage Emails" in content

    def test_profile_password_change_link(self, authenticated_client):
        """Profile shows password change links."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        content = response.content.decode()
        assert "Change Password" in content

    def test_profile_navigation_elements(self, authenticated_client):
        """Profile shows correct navigation elements."""
        url = reverse("users:profile")
        response = authenticated_client.get(url)

        content = response.content.decode()
        assert "Profile" in content
        assert "Sign Out" in content

    def test_email_management_view_accessible(self, authenticated_client):
        """Email management view is accessible via HTMX."""
        url = reverse("users:email_management")
        response = authenticated_client.get(url)
        assert response.status_code == 200

    def test_email_management_requires_login(self, client):
        """Email management requires authentication."""
        url = reverse("users:email_management")
        response = client.get(url)
        assert response.status_code == 302
        assert "/auth/login/" in response.url

    def test_profile_edit_requires_login(self, client):
        """Profile edit requires authentication."""
        url = reverse("users:profile_edit")
        response = client.get(url)
        assert response.status_code == 302
        assert "/auth/login/" in response.url
