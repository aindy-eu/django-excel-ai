# Django Excel AI Validator - Project Structure

## Project Root Files

```
├── .devcontainer/              # VSCode DevContainer configuration
│   ├── Dockerfile
│   ├── devcontainer.json
│   └── docker-compose.yml
├── .djlintrc                   # Django template linter config
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore patterns
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── CLAUDE.md                   # Claude AI assistant instructions
├── LICENSE.md                  # MIT License
├── README.md                   # Project documentation
├── conftest.py                 # Pytest configuration
├── dev-start.sh                # Development startup script
├── manage.py                   # Django management script
└── pytest.ini                  # Pytest settings
```

## Claude Documentation & Framework

```
.claude/
├── analysis/                   # Code and documentation analysis
│   ├── code/
│   │   ├── 01-project-overview.md
│   │   ├── 02-technical-architecture.md
│   │   ├── 03-codebase-structure.md
│   │   ├── 04-development-operations.md
│   │   ├── 05-code-quality.md
│   │   ├── 06-security-analysis.md
│   │   ├── 07-performance-scalability.md
│   │   └── README.md
│   └── docs/
│       ├── CLAUDE.md.verification.md
│       ├── LICENSE.md.verification.md
│       ├── README.md.verification.md
│       ├── VERIFICATION-SUMMARY.md
│       └── [other verification files]
├── commands/                   # Custom Claude commands
│   ├── django-code-analysis.md
│   └── django-docs-analysis.md
├── handovers/                  # AI handover documents
│   ├── 20250915-enterprise-structure-auth.md
│   ├── 20250915-initial-setup.md
│   ├── 20250917-avatar-upload-feature.md
│   ├── 20250917-us008-ai-excel-validation.md
│   ├── 20250919-doc-verification.md
│   ├── 20250920-documentation-cleanup.md
│   └── README.md
├── reviews/                    # Code review documents
│   ├── US-001-003-project-review-20250915.md
│   ├── US-005-review-20250917.md
│   ├── US-006-review-20250917.md
│   ├── US-007-review-20250917.md
│   └── US-008-review-20250918.md
└── scruaim/                    # Scruaim framework
    ├── README.md
    ├── backlog/
    │   ├── README.md
    │   ├── backlog.md
    │   ├── completed.md
    │   └── in-progress.md
    └── user-stories/
        ├── INSTRUCTIONS.md
        ├── README.md
        ├── STORY-REVIEW.md
        ├── done/
        │   ├── US-001-authentication-app-setup.md
        │   ├── US-002-allauth-custom-templates.md
        │   ├── US-003-user-app-structure.md
        │   ├── US-005-avatar-upload-feature.md
        │   ├── US-006-excel-upload-display.md
        │   ├── US-007-claude-sdk-setup.md
        │   └── US-008-ai-excel-validation.md
        ├── draft/
        │   └── .gitkeep
        └── todo/
            ├── US-004-security-configuration-fix.md
            ├── US-009-admin-consistency-pattern.md
            ├── US-010-ci-cd-pipeline-setup.md
            ├── US-011-explain-scruaim-framework.md
            ├── US-012-explain-ai-handovers.md
            ├── US-013-explain-slash-commands.md
            └── US-042-fix-allauth-deprecated-settings.md
```

## Django Applications

```
apps/                           # Django applications
├── __init__.py
│
├── authentication/             # Allauth integration
│   ├── __init__.py
│   ├── adapters.py            # Custom authentication adapters
│   ├── admin.py               # Django admin configuration
│   ├── apps.py                # App configuration
│   ├── urls.py                # URL routing
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   └── tests/
│       ├── __init__.py
│       └── test_auth.py
│
├── core/                       # Core utilities and services
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py              # Shared models
│   ├── views.py               # Base views
│   ├── management/
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── test_ai.py     # AI service test command
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py      # Claude AI service
│   └── tests/
│       ├── __init__.py
│       └── test_ai_service.py
│
├── dashboard/                  # Main dashboard app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── templates/
│   │   └── dashboard/
│   │       └── index.html     # Dashboard main page
│   └── tests/
│       ├── __init__.py
│       └── test_views.py
│
├── excel_manager/              # Excel file management
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py               # Upload forms
│   ├── models.py              # ExcelFile, AIValidation models
│   ├── urls.py
│   ├── views.py               # Upload, validation views
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_aivalidation.py
│   ├── services/
│   │   └── __init__.py
│   ├── templates/
│   │   └── excel_manager/
│   │       ├── index.html
│   │       ├── detail.html
│   │       └── partials/      # HTMX partials
│   │           ├── _ai_validation_error.html
│   │           ├── _ai_validation_loading.html
│   │           ├── _ai_validation_result.html
│   │           ├── _data_table.html
│   │           ├── _file_list.html
│   │           └── _upload_area.html
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py        # Test fixtures
│       ├── test_ai_validation.py
│       └── test_views.py
│
└── users/                      # User management
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py               # Profile forms
    ├── models.py              # User, UserProfile models
    ├── signals.py             # User signal handlers
    ├── urls.py
    ├── views.py               # Profile views
    ├── migrations/
    │   ├── __init__.py
    │   ├── 0001_initial.py
    │   ├── 0002_alter_user_managers.py
    │   ├── 0003_remove_user_phone_userprofile_first_name_and_more.py
    │   ├── 0004_migrate_names_to_profile.py
    │   └── 0005_remove_user_names.py
    ├── templates/
    │   └── users/
    │       ├── profile.html
    │       ├── profile_edit.html
    │       └── partials/
    │           ├── _profile_detail_item.html
    │           ├── _profile_info_card.html
    │           └── _settings_card.html
    └── tests/
        ├── __init__.py
        ├── factories.py       # Test factories
        ├── test_avatar_upload.py
        ├── test_models.py
        └── test_views.py
```

## Configuration

```
config/                         # Django configuration
├── __init__.py
├── asgi.py                    # ASGI application
├── wsgi.py                    # WSGI application
├── urls.py                    # Main URL configuration
└── settings/
    ├── __init__.py
    ├── base.py                # Base settings
    ├── development.py         # Development settings
    ├── production.py          # Production settings
    └── test.py                # Test settings
```

## Libraries & Utilities

```
libs/                           # Pure Python utilities
├── __init__.py
├── decorators/
│   └── __init__.py
├── middleware/
│   └── __init__.py
├── utils/
│   └── __init__.py
└── validators/
    └── __init__.py
```

## Documentation

```
docs/                           # Project documentation
├── README.md                   # Documentation overview
├── admin-strategy.md           # Admin panel strategy
├── architecture.md             # System architecture
├── development.md              # Development guide
├── rails-to-django.md          # Rails to Django mapping
├── technical.md                # Technical specifications
├── claude-sdk/                 # Claude SDK documentation
│   ├── README.md
│   ├── ai-validation-architecture.md
│   ├── billing-validation.md
│   ├── cost-optimization-strategies.md
│   ├── features-showcase.md
│   └── integration-guide.md
├── frontend/                   # Frontend documentation
│   ├── README.md
│   ├── htmx-patterns.md
│   ├── javascript.md
│   ├── partials.md
│   └── tailwind.md
├── images/                     # Documentation images
│   ├── excel-manager-ai-validation.jpg
│   ├── excel-manager-excel-details.jpg
│   ├── excel-manager.jpg
│   └── user-profile.jpg
├── testing/                    # Testing documentation
│   └── README.md
└── tools/                      # Tool-specific docs
    └── claude-opus-4.1/
        ├── README.md
        ├── ai-handovers.md
        ├── scruaim-framework.md
        └── slash-commands.md
```

## Templates

```
templates/                      # Global templates
├── base.html                   # Base template
├── home.html                   # Homepage
├── about.html                  # About page
├── account/                    # Allauth templates
│   ├── email.html
│   ├── login.html
│   ├── password_change.html
│   └── signup.html
└── partials/                   # Reusable partials
    ├── auth/
    │   └── _buttons.html
    ├── forms/
    │   └── _field.html
    ├── htmx/
    │   ├── _avatar_upload.html
    │   ├── _email_management.html
    │   ├── _email_management_card.html
    │   ├── _email_settings_default.html
    │   └── _profile_cards.html
    ├── navigation/
    │   ├── _main.html
    │   ├── _mobile_menu.html
    │   ├── _nav_authenticated.html
    │   ├── _nav_guest.html
    │   └── _user_menu.html
    └── ui/
        └── _theme_toggle.html
```

## Static Assets

```
static/                         # Static files
├── app-favicon-180.webp       # Application favicon
└── js/
    ├── alpine/                 # Alpine.js components
    │   └── components/
    │       ├── avatarUpload.js
    │       ├── dropdown.js
    │       ├── excelUpload.js
    │       └── theme.js
    └── utils/
        └── csrf.js             # CSRF utilities
```

## Frontend Build

```
static_src/                     # Frontend source files
├── package.json                # Node dependencies
├── postcss.config.js           # PostCSS configuration
├── tailwind.config.js          # Tailwind CSS configuration
└── src/
    └── styles.css              # Main stylesheet
```

## Requirements

```
requirements/                   # Python dependencies
├── base.txt                    # Base requirements
├── base.lock                   # Locked base versions
├── development.txt             # Development requirements
├── development.lock            # Locked dev versions
├── production.txt              # Production requirements
├── production.lock             # Locked prod versions
├── test.txt                    # Test requirements
└── test.lock                   # Locked test versions
```

## Key Features

### 1. **Authentication System**
- Email-based authentication (no usernames)
- Django-allauth integration
- Custom user model with profile
- Avatar upload functionality

### 2. **Excel Management**
- File upload with drag-and-drop
- Data preview and parsing
- AI-powered validation using Claude Sonnet 4
- Real-time validation status updates via HTMX

### 3. **Frontend Stack**
- HTMX for hypermedia interactions
- Alpine.js for reactive components
- Tailwind CSS for styling
- No SPA framework (React/Vue)

### 4. **Testing Infrastructure**
- Pytest with factories
- 86% code coverage
- Unit and integration tests
- Test fixtures and factories

### 5. **Development Tools**
- Pre-commit hooks (Black, Ruff, MyPy)
- pip-tools for dependency management
- DevContainer support
- Claude AI assistant integration

## Project Statistics

- **Django Version**: 5.1
- **Python Version**: 3.11+
- **Test Coverage**: 86%
- **Apps**: 5 (authentication, core, dashboard, excel_manager, users)
- **Models**: User, UserProfile, ExcelFile, AIValidation
- **Templates**: 30+ files with partials
- **Documentation**: Comprehensive technical and user docs

## License

MIT License - See [LICENSE.md](./LICENSE.md) for details.

---

*Generated: 2025-09-21*
*Project: Django Excel AI Validator*
*Framework: Scruaim Development Framework*