# Architecture Documentation

## Directory Structure

```
django-excel-ai/
├── apps/                  # Business applications
│   ├── core/             # Django-specific utilities (Two Scoops pattern)
│   │   ├── models.py     # Abstract base models (TimeStampedModel)
│   │   ├── services/     # AI service integration (Claude SDK)
│   │   ├── management/   # Management commands
│   │   └── tests/        # Core app tests
│   ├── users/            # Custom User model (email-based, no username)
│   │   └── tests/        # User tests & factories
│   ├── authentication/   # allauth integration & auth flows
│   │   └── tests/        # Auth flow tests
│   ├── dashboard/        # Main application dashboard
│   │   └── tests/        # Dashboard view tests
│   └── excel_manager/    # Excel upload and AI validation
│       └── tests/        # Excel manager tests
│
├── libs/                 # Standalone Python packages (placeholder structure)
│   ├── utils/           # (Empty - future Python utilities)
│   ├── validators/      # (Empty - future validation logic)
│   ├── decorators/      # (Empty - future decorators)
│   └── middleware/      # (Empty - future middleware)
│
├── config/              # Django project configuration
│   ├── settings/
│   │   ├── base.py     # Common settings
│   │   ├── development.py
│   │   ├── production.py
│   │   └── test.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── requirements/        # pip-tools managed dependencies
│   ├── base.txt         # Core dependencies (source)
│   ├── base.lock        # Locked versions for reproducibility
│   ├── development.txt  # Dev dependencies (source)
│   ├── development.lock # Dev locked versions
│   ├── production.txt   # Prod dependencies (source)
│   ├── production.lock  # Prod locked versions
│   ├── test.txt         # Test dependencies (source)
│   └── test.lock        # Test locked versions
│
├── static_src/         # Tailwind CSS source files
├── static/             # Development static files
├── staticfiles/        # Production collected static (git-ignored)
├── templates/          # Global templates
├── media/              # User uploads
└── docs/               # Project documentation
```

## Design Decisions

### Why apps/core AND libs/?

**apps/core**: Django-specific utilities and services
- Following Two Scoops of Django best practice
- Contains abstract models (TimeStampedModel)
- AI service integration (Claude SDK)
- Management commands for testing
- Note: utils.py and mixins.py planned but not yet implemented

**libs/**: Placeholder for pure Python utilities
- Structure created for future expansion
- Currently empty (only __init__.py files)
- Will house Django-independent code
- Reserved for extractable packages

### Custom User Model

- **Email as primary identifier** (no username field)
- Located in `apps/users`
- Configured: `AUTH_USER_MODEL = 'users.User'`
- allauth: `ACCOUNT_USER_MODEL_USERNAME_FIELD = None`

### Authentication Architecture

- `apps/authentication` handles allauth integration
- Separate from `apps/users` for cleaner separation:
  - **users**: Data model, admin, user management
  - **authentication**: Auth flows, templates, adapters

### Settings Strategy

Split settings by environment:
- `base.py`: Common configuration
- `development.py`: Local development
- `production.py`: Production deployment
- `test.py`: Test runner configuration

### Static Files Architecture

Three-tier approach:
1. **static_src/**: Tailwind source files and build config
2. **static/**: Compiled assets for development
3. **staticfiles/**: Collected assets for production

### Testing Architecture

Enterprise pytest-based testing:
- **Framework**: pytest (not Django TestCase)
- **Structure**: `apps/*/tests/` folders (not tests.py files)
- **Factories**: factory-boy for test data generation
- **Coverage**: 70% minimum requirement
- **Markers**: unit, integration, auth, model, view, api
- **Config**: pytest.ini with enterprise settings

## Architectural Principles

1. **Single Responsibility**: Each app has one clear purpose
2. **DRY (Don't Repeat Yourself)**: Abstract models and utilities
3. **Separation of Concerns**: Clear boundaries between apps
4. **12-Factor App**: Environment-based configuration
5. **Security First**: No secrets in code, email-based auth
6. **Scalability**: Modular design for easy extension

## Implementation Status

### Fully Implemented ✅
- Custom email-based User model
- TimeStampedModel abstract base
- Authentication/Users app separation
- pytest testing framework with 70% minimum
- All 5 Django apps (core, users, authentication, dashboard, excel_manager)
- AI service layer in core/services/
- Environment-based settings split
- pip-tools dependency management with lock files

### Planned/Placeholder 🚧
- libs/ utilities (structure exists but empty)
- apps/core/utils.py (documented but not created)
- apps/core/mixins.py (documented but not created)

### Key Apps Overview
- **core**: Base models, AI services, management commands
- **users**: Custom User model, profiles, avatar upload
- **authentication**: Django-allauth integration, custom adapters
- **dashboard**: Main authenticated user interface
- **excel_manager**: Excel upload, processing, and AI validation