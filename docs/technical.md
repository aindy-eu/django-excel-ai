# Technical Specifications

## Stack

### Backend
- **Framework**: Django 5.1 (constrained to <5.2)
- **Database**: PostgreSQL 15+ with psycopg3
- **Authentication**: django-allauth 65.0+
- **AI Integration**: Anthropic Claude SDK
- **Excel Processing**: openpyxl
- **File Validation**: python-magic
- **API**: Django REST Framework (planned, not implemented)
- **Task Queue**: Redis ready, Celery planned

### Frontend
- **CSS Framework**: Tailwind CSS 3.4.14
- **Build Tools**: PostCSS, Autoprefixer
- **JavaScript**: HTMX 1.9 + Alpine.js 3.x
- **Architecture**: Server-first, progressive enhancement
- **Icons**: Heroicons (if used)
- **Forms**: Crispy Forms with Tailwind theme

### Infrastructure
- **Server**: Gunicorn (production)
- **Static Files**: WhiteNoise with compression
- **Environment**: Python 3.11+ (tested with 3.13)
- **Container**: DevContainer available, Docker not configured
- **Monitoring**: Sentry SDK, django-prometheus (production)
- **Environment Management**: python-dotenv + os.environ

## Key Configuration

### Custom User Model
```python
# apps/users/models.py
class User(AbstractUser):
    username = None  # Removed
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
```

### Authentication Settings
```python
# config/settings/base.py
AUTH_USER_MODEL = 'users.User'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {'email'}  # Modern approach
# Note: Deprecated settings still present (US-042 todo):
# ACCOUNT_EMAIL_REQUIRED, ACCOUNT_USERNAME_REQUIRED,
# ACCOUNT_AUTHENTICATION_METHOD
```

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### Static Files Configuration
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Tailwind CSS output
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

## Security Features

### Authentication
- Email-based authentication (no usernames)
- Password validation rules enforced
- Optional email verification
- Session-based authentication
- CSRF protection enabled

### Headers & Middleware
```python
# Production settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Environment Variables
- Secrets in `.env` file (never committed)
- Different settings per environment
- `django-environ` for env management

## Performance Optimizations

### Database
- Database indexes on frequently queried fields
- Query optimization with `select_related()` and `prefetch_related()`
- Connection pooling in production

### Static Files
- Tailwind CSS JIT mode for smaller bundles
- WhiteNoise for efficient static serving
- Browser caching headers

### Caching Strategy
```python
# Production configuration (already implemented)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'django_cache',
    }
}
```

## API Design (Planned - Not Implemented)

### RESTful Endpoints
```
/api/v1/users/          # User management
/api/v1/auth/           # Authentication
/api/v1/dashboard/      # Dashboard data
```

### Versioning Strategy
- URL path versioning (`/api/v1/`)
- Backward compatibility for 2 versions
- Deprecation notices in headers

## Monitoring & Logging

### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Health Checks (Planned - Not Implemented)
- `/health/` - Application health (TODO)
- `/ready/` - Database connectivity (TODO)
- `/metrics/` - Prometheus metrics (django-prometheus installed)

## Implementation Status

### Currently Implemented ✅
- Django 5.1 application with PostgreSQL
- Email-based authentication with django-allauth
- HTMX + Alpine.js for dynamic UI
- Tailwind CSS with PostCSS pipeline
- Claude AI integration for Excel validation
- Excel file processing with openpyxl
- WhiteNoise for static files
- Redis caching configuration (production)
- Comprehensive logging with AI service tracking
- Development tools (pytest, black, ruff, mypy)

### Planned/Not Implemented 🚧
- Django REST Framework API
- Celery task queue (Redis is ready)
- Health check endpoints
- Docker configuration (only DevContainer exists)
- Nginx reverse proxy setup
- Prometheus metrics endpoint

### Deprecated/To Fix ⚠️
- Remove deprecated allauth settings (US-042)
- Strengthen SECRET_KEY handling (US-004)
- Implement proper health checks