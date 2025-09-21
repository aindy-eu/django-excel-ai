from django.contrib import admin
from django.conf import settings

# Only register admin in development
if settings.DEBUG or getattr(settings, "ADMIN_ENABLED", False):
    # Future: Register authentication-related models here
    pass
