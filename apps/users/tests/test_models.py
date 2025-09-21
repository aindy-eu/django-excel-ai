"""
Tests for User and UserProfile models.
Phase 1: Core model testing with email authentication.
"""

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.users.tests.factories import (
    UserFactory,
    UserProfileFactory,
    UserWithProfileFactory,
)
from apps.users.models import UserProfile

User = get_user_model()


@pytest.mark.model
@pytest.mark.auth
class TestUserModel:
    """Test custom User model with email authentication."""

    def test_create_user_with_email(self, db):
        """User can be created with email as primary identifier."""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("testpass123")

    def test_email_is_username_field(self, db):
        """Email is used as USERNAME_FIELD."""
        assert User.USERNAME_FIELD == "email"
        assert "email" in User.REQUIRED_FIELDS or User.USERNAME_FIELD == "email"

    def test_no_username_field(self, db):
        """User model has username set to None."""
        user = UserFactory()
        assert user.username is None

    def test_email_must_be_unique(self, db):
        """Email addresses must be unique."""
        User.objects.create_user(email="duplicate@example.com", password="test")
        with pytest.raises(IntegrityError):
            User.objects.create_user(email="duplicate@example.com", password="test")

    def test_email_normalized(self, db):
        """Email addresses are normalized."""
        user = User.objects.create_user(
            email="TEST@EXAMPLE.COM", password="testpass123"
        )
        assert user.email == "TEST@example.com"

    def test_create_superuser(self, db):
        """Superuser creation sets correct flags."""
        admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.is_active is True

    def test_user_string_representation(self, db):
        """User string representation is email."""
        user = UserFactory(email="display@example.com")
        assert str(user) == "display@example.com"

    def test_user_full_name(self, db):
        """User full name combines first and last names from profile."""
        user = UserWithProfileFactory()
        user.profile.first_name = "John"
        user.profile.last_name = "Doe"
        user.profile.save()
        assert user.get_full_name() == "John Doe"

    def test_user_short_name(self, db):
        """User short name is first name from profile."""
        user = UserWithProfileFactory()
        user.profile.first_name = "Jane"
        user.profile.save()
        assert user.get_short_name() == "Jane"

    def test_user_factory_creates_valid_user(self, db):
        """UserFactory creates valid user instances."""
        user = UserFactory()
        assert user.pk is not None
        assert user.email is not None
        assert User.objects.filter(email=user.email).exists()

    def test_user_factory_with_password(self, db):
        """UserFactory can set custom password."""
        user = UserFactory(password="custompass123")
        assert user.check_password("custompass123")

    def test_user_custom_fields(self, db):
        """User model has custom fields."""
        user = UserFactory(is_verified=True, ip_address="192.168.1.1")
        assert user.is_verified is True
        assert user.ip_address == "192.168.1.1"

    def test_user_timestamps(self, db):
        """User model has timestamp fields."""
        user = UserFactory()
        assert user.date_joined is not None
        assert user.last_activity is not None


@pytest.mark.model
class TestUserProfile:
    """Test UserProfile model."""

    def test_profile_creation(self, db):
        """UserProfile is created automatically for a user."""
        user = UserFactory()
        # Profile should be created automatically by signal
        assert hasattr(user, "profile")
        user.profile.bio = "Test bio"
        user.profile.save()
        assert user.profile.bio == "Test bio"

    def test_profile_one_to_one_relationship(self, db):
        """Each user can have only one profile."""
        user = UserFactory()
        # Profile is already created by signal
        assert user.profile is not None
        with pytest.raises(IntegrityError):
            UserProfile.objects.create(user=user)

    def test_profile_string_representation(self, db):
        """Profile string representation includes user email."""
        user = UserFactory(email="profile@example.com")
        profile = UserProfileFactory(user=user)
        assert user.email in str(profile)

    def test_profile_factory_creates_valid_profile(self, db):
        """UserProfileFactory creates valid profile instances."""
        profile = UserProfileFactory()
        assert profile.pk is not None
        assert profile.user is not None
        assert UserProfile.objects.filter(pk=profile.pk).exists()

    def test_user_with_profile_factory(self, db):
        """UserWithProfileFactory creates user and profile."""
        user = UserWithProfileFactory()
        assert user.pk is not None
        assert hasattr(user, "profile")
        assert user.profile.pk is not None

    def test_profile_optional_fields(self, db):
        """Profile optional fields can be null/blank."""
        user = UserFactory()
        profile = user.profile
        profile.bio = ""
        profile.date_of_birth = None
        profile.phone_number = ""
        profile.save()
        assert profile.bio == ""
        assert profile.date_of_birth is None
        assert profile.phone_number == ""

    def test_profile_cascade_delete(self, db):
        """Profile is deleted when user is deleted."""
        user = UserWithProfileFactory()
        profile_id = user.profile.id
        user.delete()
        assert not UserProfile.objects.filter(id=profile_id).exists()
