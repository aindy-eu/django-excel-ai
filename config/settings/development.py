"""
Development settings - unsuitable for production
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Admin enabled in development
ADMIN_ENABLED = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '.localhost']

# Development-specific installed apps
INSTALLED_APPS += [
    'django_extensions',  # Useful development tools
] if 'django_extensions' in sys.modules else []

# Internal IPs for django-debug-toolbar and browser-reload
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files serving
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Disable caching in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# CORS settings for development (if needed)
CORS_ALLOW_ALL_ORIGINS = True

# Session settings for development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Development logging
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

# SQL query logging in development
LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'level': 'DEBUG' if DEBUG else 'INFO',
    'propagate': False,
}

# Tailwind CSS is now handled as a build tool, not a Django app

# Authentication settings for development
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # No email verification in dev
ACCOUNT_ALLOW_SIGNUP = True  # Allow signups in dev

print("🚀 Running in DEVELOPMENT mode")