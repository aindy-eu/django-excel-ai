"""
Production settings
"""

from .base import *
import os

# Security
DEBUG = False

# Admin disabled in production
ADMIN_ENABLED = False  # Or use environment variable for emergency access
# ADMIN_ENABLED = os.environ.get('EMERGENCY_ADMIN', 'False') == 'True'

# Must be set in production
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static files with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_AUTOREFRESH = False

# Production database with connection pooling
DATABASES['default'].update({
    'CONN_MAX_AGE': 600,
    'OPTIONS': {
        'connect_timeout': 10,
        'options': '-c statement_timeout=30000'
    }
})

# Cache configuration (Redis recommended)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'django_cache',
        'TIMEOUT': 300,
    }
}

# Authentication settings for production
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Require email verification
ACCOUNT_ALLOW_SIGNUP = os.environ.get('ALLOW_SIGNUP', 'False') == 'True'
ACCOUNT_SESSION_REMEMBER = False  # Don't remember sessions in production

# Rate limiting for authentication
AXES_ENABLED = True  # Enable django-axes for brute force protection
AXES_FAILURE_LIMIT = 5  # Lock after 5 failed attempts
AXES_COOLOFF_TIME = 1  # Hours to wait after lockout

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Production logging
LOGGING['handlers']['file']['level'] = 'WARNING'
LOGGING['handlers']['file']['filename'] = '/var/log/django/app.log'

# Sentry error tracking (optional)
if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.01,
        send_default_pii=False,
        environment='production',
    )

print("🔐 Running in PRODUCTION mode")