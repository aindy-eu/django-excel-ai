"""
Test settings - optimized for test performance
"""

from .base import *

# Test configuration
DEBUG = False
TESTING = True

# Use in-memory database for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Fast password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Media files for testing
MEDIA_ROOT = BASE_DIR / 'test_media'

# Disable logging during tests
LOGGING_CONFIG = None

# Celery settings for testing (if using Celery)
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

print("🧪 Running in TEST mode")