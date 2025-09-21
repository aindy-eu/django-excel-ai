# Codebase Structure - Code Analysis

## Directory Tree with File Counts

```
.
├── apps/                    # 52 Python files (excluding migrations)
│   ├── authentication/      # Email-based auth flows
│   ├── core/               # Shared services and utilities
│   ├── dashboard/          # Main application interface
│   ├── excel_manager/      # Excel file processing
│   └── users/              # User management and profiles
├── config/                 # Django project configuration
│   ├── settings/           # Environment-specific settings
│   │   ├── base.py        # Shared configuration
│   │   ├── development.py # Dev settings
│   │   ├── production.py  # Production settings
│   │   └── test.py        # Test configuration
│   ├── asgi.py            # ASGI application
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application
├── libs/                   # Pure Python utilities
│   ├── decorators/         # Custom decorators
│   ├── middleware/         # Custom middleware
│   ├── utils/              # Utility functions
│   └── validators/         # Custom validators
├── templates/              # Global Django templates
│   ├── account/            # Allauth override templates
│   └── partials/           # Reusable template fragments
├── static_src/             # Frontend source files
│   ├── css/                # Tailwind CSS source
│   ├── node_modules/       # NPM packages
│   └── src/                # JavaScript source
├── staticfiles/            # Compiled static files
│   ├── admin/              # Django admin assets
│   ├── css/                # Compiled CSS
│   └── js/                 # JavaScript files
├── media/                  # User uploads
│   ├── avatars/            # User profile pictures
│   └── excel_uploads/      # Uploaded Excel files
├── requirements/           # Dependency management
│   ├── base.txt            # Core dependencies
│   ├── base.lock           # Locked versions
│   ├── development.txt     # Dev dependencies
│   ├── development.lock    # Dev locked versions
│   ├── production.txt      # Prod dependencies
│   ├── production.lock     # Prod locked versions
│   └── test.lock           # Test locked versions
└── manage.py               # Django management script
```

## Module Dependencies (Import Analysis)

### Core Import Patterns
```python
# Django imports (most common)
from django.db import models
from django.views.generic import TemplateView, FormView, DetailView
from django.contrib.auth import get_user_model
from django.conf import settings

# Internal app imports
from apps.core.services.ai_service import AIService
from apps.users.models import User
from apps.excel_manager.models import ExcelFile

# Third-party imports
from anthropic import Anthropic
import pytest
from unittest.mock import patch, MagicMock
```

### Dependency Graph
```
config.urls
    ├── apps.authentication.urls
    ├── apps.dashboard.urls
    ├── apps.excel_manager.urls
    └── apps.users.urls

apps.excel_manager
    ├── apps.core.services (AI service)
    ├── django.contrib.auth (authentication)
    └── libs.utils (utilities)

apps.core.services
    ├── anthropic (AI provider)
    └── django.conf.settings (configuration)

apps.users
    ├── django.contrib.auth.models
    └── allauth.account (authentication)
```

## Entry Points

### Primary Entry Point
```python
manage.py  # Django management command
    - runserver: Development server
    - migrate: Database migrations
    - test: Run test suite
    - collectstatic: Gather static files
```

### WSGI/ASGI Entry Points
```python
config/wsgi.py   # Production WSGI server
config/asgi.py   # Async ASGI server
```

### URL Entry Points
```python
config/urls.py  # Root URL configuration
    "/" → Dashboard (requires login)
    "/auth/" → Authentication flows
    "/excel/" → Excel management
    "/users/" → User profiles
    "/admin/" → Django admin (DEBUG only)
```

## Configuration Files

### Python Configuration
```bash
manage.py                  # Django CLI
conftest.py               # Pytest configuration
.pre-commit-config.yaml   # Git hooks
.djlintrc                 # Django template linting
pyproject.toml            # (Not found - uses requirements/)
```

### Frontend Configuration
```bash
static_src/package.json   # NPM dependencies
static_src/tailwind.config.js  # Tailwind CSS
```

### Environment Configuration
```bash
.env                      # Local environment variables
.env.example             # Environment template
```

## Execution Flow Trace

### Request Lifecycle
1. **Entry**: `wsgi.py` or `asgi.py`
2. **Middleware Pipeline**:
   ```python
   SecurityMiddleware → WhiteNoiseMiddleware → SessionMiddleware
   → CommonMiddleware → CsrfViewMiddleware → AuthenticationMiddleware
   → MessageMiddleware → XFrameOptionsMiddleware → BrowserReloadMiddleware
   → HtmxMiddleware → AccountMiddleware
   ```
3. **URL Routing**: `config.urls` → app urls → view
4. **View Processing**:
   - Authentication check (LoginRequiredMixin)
   - Business logic execution
   - Service layer calls (e.g., AIService)
   - Template rendering
5. **Response**: HTML with HTMX attributes

### Excel Upload Flow
```python
1. ExcelUploadView.post()
2. ExcelForm.validate()
3. ExcelFile.save() (model)
4. File saved to media/excel_uploads/
5. Redirect to ExcelDetailView
6. Optional: ValidateWithAIView (async)
```

## Code Organization Patterns

### App Structure (Standard Django MVT)
```
apps/<app_name>/
├── __init__.py          # Package marker
├── admin.py            # Django admin config
├── apps.py             # App configuration
├── forms.py            # Django forms
├── models.py           # Database models
├── urls.py             # URL patterns
├── views.py            # View classes/functions
├── services/           # Business logic (optional)
├── migrations/         # Database migrations
├── tests/              # Test suite
│   ├── factories.py    # Test data factories
│   ├── test_models.py  # Model tests
│   ├── test_views.py   # View tests
│   └── test_services.py # Service tests
├── templates/<app>/    # App-specific templates
└── static/<app>/       # App-specific static files
```

### Dead Code Detection

#### Potentially Unused Directories
```bash
./libs/decorators/   # No imports found
./libs/middleware/   # No custom middleware in settings
./libs/validators/   # No validator imports found
./venv/             # Virtual environment (should be in .gitignore)
```

#### Active Service Layers
```python
apps/core/services/ai_service.py  # AI integration (actively used)
apps/excel_manager/services/      # Excel processing services
```

## File Statistics

### Python Files Distribution
```
Total Python files: 5,839
├── Application code: 52 files
├── Migrations: ~12 files
├── Tests: ~30 files
├── Django/libs: 5,700+ files (venv + staticfiles)
```

### Template Files
```bash
Global templates: ./templates/
App templates: ./apps/*/templates/
HTMX usage: 5 references found
```

### Static Assets
```
JavaScript: Alpine.js components
CSS: Tailwind CSS compiled
Images: User avatars, icons
Admin: Django admin assets
```