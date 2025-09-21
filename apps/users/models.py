import os
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom manager for User model with email as identifier."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model for enterprise requirements.
    Email as primary identifier instead of username.
    """

    # Remove username field and use email as unique identifier
    username = None
    # Remove first_name and last_name fields (moved to UserProfile for GDPR)
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), unique=True)

    # Additional fields for enterprise needs
    is_verified = models.BooleanField(
        default=False, help_text="Email verification status"
    )

    # Audit fields
    last_activity = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # Use email as the unique identifier
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email and password are required by default

    # Use custom manager
    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["is_active", "is_verified"]),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return full name from profile or email."""
        if hasattr(self, "profile"):
            full_name = f"{self.profile.first_name} {self.profile.last_name}".strip()
            return full_name if full_name else self.email
        return self.email

    def get_short_name(self):
        """Return first name from profile or email prefix."""
        if hasattr(self, "profile") and self.profile.first_name:
            return self.profile.first_name
        return self.email.split("@")[0]


class UserProfile(models.Model):
    """
    Extended user profile for additional data.
    Separated to keep User model clean and for future encryption needs.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Personal Information (PII - GDPR relevant)
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("first name"),
        help_text="To be encrypted in production",
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("last name"),
        help_text="To be encrypted in production",
    )
    phone_number = models.CharField(
        max_length=20, blank=True, help_text="To be encrypted in production"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    # Bio and preferences
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    # Settings
    timezone = models.CharField(max_length=50, default="UTC")
    language = models.CharField(max_length=10, default="en")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return f"Profile for {self.user.email}"

    def get_full_name(self):
        """Return the full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.user.email

    def get_display_name(self):
        """Return a display name for the user."""
        if self.first_name:
            return self.first_name
        return self.user.email.split("@")[0]

    def delete_old_avatar(self):
        """Delete the old avatar file from storage."""
        if self.pk:
            try:
                old_profile = UserProfile.objects.get(pk=self.pk)
                if old_profile.avatar and old_profile.avatar != self.avatar:
                    if os.path.isfile(old_profile.avatar.path):
                        os.remove(old_profile.avatar.path)
            except UserProfile.DoesNotExist:
                pass


@receiver(pre_save, sender=UserProfile)
def delete_old_avatar_on_change(sender, instance, **kwargs):
    """Delete old avatar file when a new one is uploaded."""
    if instance.pk:
        try:
            old_profile = UserProfile.objects.get(pk=instance.pk)
            if old_profile.avatar and old_profile.avatar != instance.avatar:
                if os.path.isfile(old_profile.avatar.path):
                    os.remove(old_profile.avatar.path)
        except UserProfile.DoesNotExist:
            pass
