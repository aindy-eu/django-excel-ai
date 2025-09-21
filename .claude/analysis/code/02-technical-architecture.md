# Technical Architecture - Code Analysis

## Tech Stack (From Actual Imports)

### Backend Framework
```python
# Found in requirements/base.txt
Django >= 5.1, < 5.2  # Latest Django LTS
psycopg[binary] >= 3.2  # PostgreSQL adapter
django-environ >= 0.11  # Environment configuration
```

### Frontend Technologies
```python
django-htmx >= 1.19.0     # Server-side interactivity
whitenoise >= 6.7         # Static file serving
Pillow >= 10.4           # Image processing
django-crispy-forms >= 2.3  # Form rendering
crispy-tailwind >= 1.0    # Tailwind CSS integration
```

### Authentication System
```python
django-allauth >= 65.0  # Comprehensive auth solution
# Custom email-based authentication (no username field)
```

### AI Integration
```python
# From imports in apps/core/services/ai_service.py
from anthropic import Anthropic  # Claude AI API
```

## Architecture Patterns (From Code Organization)

### Application Structure
```
Monolithic Django Application
├── MVT Pattern (Model-View-Template)
├── Service Layer (apps/core/services/)
├── Factory Pattern (tests/factories.py)
└── Repository Pattern (implicit in Django ORM)
```

### Middleware Stack (Execution Order)
```python
1. SecurityMiddleware        # Security headers
2. WhiteNoiseMiddleware      # Static file serving
3. SessionMiddleware         # Session management
4. CommonMiddleware          # Common HTTP features
5. CsrfViewMiddleware       # CSRF protection
6. AuthenticationMiddleware  # User authentication
7. MessageMiddleware        # Flash messages
8. XFrameOptionsMiddleware  # Clickjacking protection
9. BrowserReloadMiddleware  # Development hot-reload
10. HtmxMiddleware          # HTMX request detection
11. AccountMiddleware       # Allauth account management
```

## Database Architecture

### Primary Database
```python
ENGINE: 'django.db.backends.postgresql'
NAME: os.environ.get('DB_NAME', 'dashboard_db')
USER: os.environ.get('DB_USER', 'devuser')
HOST: os.environ.get('DB_HOST', 'localhost')
PORT: os.environ.get('DB_PORT', '5432')
```

### Models Found
```bash
./apps/core/models.py         # Base/utility models
./apps/users/models.py        # User and profile models
./apps/excel_manager/models.py  # Excel file tracking
```

## API Architecture

### View Types (No REST Framework Found)
```python
# Traditional Django views
ExcelManagerView(LoginRequiredMixin, TemplateView)
ExcelUploadView(LoginRequiredMixin, FormView)
ExcelDetailView(LoginRequiredMixin, DetailView)
ValidateWithAIView(LoginRequiredMixin, View)
DeleteExcelView(LoginRequiredMixin, View)

# Dashboard views
DashboardView(TemplateView)
ProfileView(TemplateView)
ProfileUpdateView(TemplateView)
```

### URL Patterns
```python
# Root patterns found
path("", DashboardView.as_view(), name="index")
path("profile/", ProfileView.as_view())
path("upload/", ExcelUploadView.as_view())
path("<int:pk>/", ExcelDetailView.as_view())
path("profile/avatar/", AvatarUploadView.as_view())
```

## External Service Integration

### AI Service (Anthropic Claude)
```python
# apps/core/services/ai_service.py
class AIService:
    - Uses Anthropic API client
    - Validates Excel data
    - Async processing capabilities
```

### File Storage
```python
# Local filesystem storage
# Excel files uploaded and stored
# Avatar images for user profiles
# Processed with Pillow for image manipulation
```

## Infrastructure Components

### Static File Handling
```python
WhiteNoise middleware for production
django_browser_reload for development
Tailwind CSS compilation (found in static_src/)
```

### Session Management
```python
Django sessions (database-backed)
CSRF protection enabled
Cookie-based authentication
```

### Configuration Management
```python
# Settings structure found
config/settings/
├── base.py        # Shared settings
├── development.py  # Dev overrides
├── production.py   # Prod settings
├── test.py        # Test configuration
```

## Security Architecture

### Authentication Flow
1. Email-based login (no username)
2. Django-allauth handles registration/login
3. LoginRequiredMixin protects views
4. Session-based authentication

### Security Middleware
- CSRF protection enabled
- Security headers via SecurityMiddleware
- XFrame options for clickjacking protection
- HTTPS enforcement in production

## Template Architecture

### Rendering Strategy
```python
# Server-side rendering with Django templates
# HTMX for partial page updates (5 references found)
# No SPA framework detected
# Alpine.js for client-side interactions (found in staticfiles/)
```

### Template Organization
```
templates/           # Global templates
apps/*/templates/    # App-specific templates
```

## Development Tools Integration

### Testing Framework
```python
pytest with coverage reporting
Factory pattern for test data
120 tests collected
86% code coverage achieved
```

### Code Quality Tools (From Config Files)
```python
.pre-commit-config.yaml  # Git hooks
.djlintrc               # Django template linting
.mypy_cache/            # Type checking
.ruff_cache/            # Python linting
```