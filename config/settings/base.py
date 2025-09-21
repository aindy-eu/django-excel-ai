"""
Base settings for Django project.
All environment-specific settings should override these base settings.
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_browser_reload',
    'crispy_forms',
    'crispy_tailwind',
    'django_htmx',
]

LOCAL_APPS = [
    'apps.users',  # MUST be first - contains custom User model
    'apps.authentication',  # Must be before allauth
    'apps.core',
    'apps.dashboard',
    'apps.excel_manager',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database - Override in environment-specific settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'dashboard_db'),
        'USER': os.environ.get('DB_USER', 'devuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'devpassword123'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model (CRITICAL - must be set before first migration)
AUTH_USER_MODEL = 'users.User'

# Sites framework
SITE_ID = 1

# Django-allauth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Custom adapter for authentication behavior
ACCOUNT_ADAPTER = 'apps.authentication.adapters.AuthenticationAdapter'

# Updated allauth settings for v65+ and custom User without username
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # We don't have username field
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True  # No confirmation page
ACCOUNT_ALLOW_SIGNUP = True  # Can be disabled in production

# Redirect URLs
# Note: These must be paths, not URL names
# They define where users go after login/logout and where to redirect for login
LOGIN_REDIRECT_URL = '/dashboard/'  # After successful login
LOGOUT_REDIRECT_URL = '/'  # After logout
LOGIN_URL = '/auth/login/'  # Where to redirect for @login_required

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        # AI Service detailed logging
        'apps.core.services.ai_service': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Anthropic SDK logging
        'anthropic': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'httpx': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Suppress noisy autoreloader messages
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# AI Configuration
AI_CONFIG = {
    'ENABLED': os.environ.get('AI_FEATURES_ENABLED', 'False') == 'True',
    'ANTHROPIC_API_KEY': os.environ.get('ANTHROPIC_API_KEY'),
    'MODEL': os.environ.get('CLAUDE_MODEL', 'claude-sonnet-4-20250514'),
    'MAX_TOKENS': int(os.environ.get('CLAUDE_MAX_TOKENS', '1000')),
    'TIMEOUT': 30,  # seconds
}