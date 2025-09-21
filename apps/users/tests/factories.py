"""
User model factories for testing.
Enterprise-ready test data generation.
"""

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.utils import timezone

from apps.users.models import User, UserProfile

fake = Faker()


class UserFactory(DjangoModelFactory):
    """Factory for User model with email authentication."""

    class Meta:
        model = User
        django_get_or_create = ("email",)
        skip_postgeneration_save = True  # Avoid deprecation warning

    email = factory.LazyAttribute(lambda _: fake.unique.email())
    is_active = True
    is_staff = False
    is_superuser = False
    is_verified = False
    last_activity = factory.LazyFunction(timezone.now)  # Use timezone-aware datetime
    ip_address = factory.Faker("ipv4")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("defaultpass123")
        self.save()  # Must explicitly save when using skip_postgeneration_save

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.groups.add(*extracted)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.user_permissions.add(*extracted)


class AdminFactory(UserFactory):
    """Factory for admin users."""

    is_staff = True
    is_superuser = True
    is_verified = True


class StaffFactory(UserFactory):
    """Factory for staff users."""

    is_staff = True
    is_verified = True


class UserProfileFactory(DjangoModelFactory):
    """Factory for UserProfile model."""

    class Meta:
        model = UserProfile
        django_get_or_create = ("user",)

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    bio = factory.Faker("text", max_nb_chars=500)
    date_of_birth = factory.Faker("date_of_birth", minimum_age=18, maximum_age=90)
    avatar = None  # Handle file uploads separately in tests
    phone_number = factory.Faker("phone_number")
    address = factory.Faker("address")
    timezone = factory.Faker("timezone")
    language = "en"


class UserWithProfileFactory(UserFactory):
    """Factory that creates a user with an associated profile."""

    class Meta:
        model = User
        skip_postgeneration_save = True  # Avoid deprecation warning

    profile = factory.RelatedFactory(
        UserProfileFactory,
        factory_related_name="user",
    )
