from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


# Only register admin in development
if settings.DEBUG or getattr(settings, "ADMIN_ENABLED", False):

    @admin.register(User)
    class UserAdmin(BaseUserAdmin):
        """Admin for custom User model."""

        fieldsets = (
            (None, {"fields": ("email", "password")}),
            (_("Account Status"), {"fields": ("is_verified",)}),
            (
                _("Permissions"),
                {
                    "fields": (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                        "groups",
                        "user_permissions",
                    ),
                },
            ),
            (
                _("Important dates"),
                {"fields": ("last_login", "date_joined", "last_activity")},
            ),
            (_("Tracking"), {"fields": ("ip_address",)}),
        )
        add_fieldsets = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": ("email", "password1", "password2"),
                },
            ),
        )
        list_display = ("email", "is_verified", "is_staff", "date_joined")
        list_filter = (
            "is_staff",
            "is_superuser",
            "is_active",
            "is_verified",
            "date_joined",
        )
        search_fields = ("email",)
        ordering = ("-date_joined",)

        # Remove username from the admin
        def get_fieldsets(self, request, obj=None):
            fieldsets = super().get_fieldsets(request, obj)
            # Remove username field if it exists
            for fieldset in fieldsets:
                if "username" in fieldset[1].get("fields", []):
                    fields = list(fieldset[1]["fields"])
                    fields.remove("username")
                    fieldset[1]["fields"] = tuple(fields)
            return fieldsets

    @admin.register(UserProfile)
    class UserProfileAdmin(admin.ModelAdmin):
        """Admin for UserProfile."""

        list_display = (
            "user",
            "get_full_name",
            "phone_number",
            "timezone",
            "language",
            "created_at",
        )
        list_filter = ("language", "timezone", "created_at")
        search_fields = ("user__email", "first_name", "last_name", "phone_number")
        readonly_fields = ("created_at", "updated_at")

        fieldsets = (
            ("User", {"fields": ("user",)}),
            (
                "Personal Information (PII)",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "phone_number",
                        "date_of_birth",
                        "address",
                    ),
                    "description": "Personal data - Will be encrypted in production (GDPR)",
                },
            ),
            ("Profile", {"fields": ("bio", "avatar")}),
            ("Preferences", {"fields": ("timezone", "language")}),
            ("Metadata", {"fields": ("created_at", "updated_at")}),
        )

        def get_full_name(self, obj):
            """Display full name in admin list."""
            return obj.get_full_name()

        get_full_name.short_description = "Full Name"
