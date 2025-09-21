"""
Root conftest.py for pytest configuration.
Enterprise-ready test fixtures and configurations.
"""
import pytest
import django
from django.conf import settings
import shutil
from pathlib import Path

# Configure Django settings before any imports
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def user_factory(db):
    """Factory for creating users with email authentication."""
    def create_user(
        email="test@example.com",
        password="testpass123",
        is_active=True,
        is_staff=False,
        is_superuser=False,
        **kwargs
    ):
        user = User.objects.create_user(
            email=email,
            password=password,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **kwargs
        )
        user.raw_password = password  # Store for test access
        return user
    return create_user


@pytest.fixture
def user(user_factory):
    """Standard test user."""
    return user_factory()


@pytest.fixture
def admin_user(user_factory):
    """Admin test user."""
    return user_factory(
        email="admin@example.com",
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def authenticated_client(client, user):
    """Client with authenticated user."""
    client.force_login(user)
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Client with authenticated admin user."""
    client.force_login(admin_user)
    return client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enable database access for all tests.
    Remove if you want explicit db marking.
    """
    pass


@pytest.fixture(autouse=True, scope='function')
def cleanup_test_media():
    """
    Clean up test media files after each test.
    Only runs for tests that create media files.
    """
    yield

    # Clean up after test
    test_media_path = Path(settings.MEDIA_ROOT)
    if test_media_path.exists() and 'test_media' in str(test_media_path):
        # Only clean if files were created during test
        if any(test_media_path.iterdir()):
            shutil.rmtree(test_media_path, ignore_errors=True)


@pytest.fixture
def api_client():
    """API test client for REST endpoints."""
    from django.test import Client

    class APIClient(Client):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.headers = {}

        def set_credentials(self, **kwargs):
            self.headers.update(kwargs)

        def request(self, **kwargs):
            kwargs.update(self.headers)
            return super().request(**kwargs)

    return APIClient()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Override django_db_setup to customize test database."""
    with django_db_blocker.unblock():
        # Clean test media before test session
        test_media_path = Path(settings.MEDIA_ROOT)
        if test_media_path.exists() and 'test_media' in str(test_media_path):
            shutil.rmtree(test_media_path, ignore_errors=True)

    yield

    # Clean test media after test session
    with django_db_blocker.unblock():
        test_media_path = Path(settings.MEDIA_ROOT)
        if test_media_path.exists() and 'test_media' in str(test_media_path):
            shutil.rmtree(test_media_path, ignore_errors=True)