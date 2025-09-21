# .scruaim Framework - Django Excel AI Validator

> Django-tailored user story framework for systematic development

## Project Profile

### Technology Stack
```yaml
# Core
Framework: Django >=5.1
Database: PostgreSQL (psycopg[binary] >=3.2)
CSS Framework: Tailwind CSS (django-tailwind >=3.8)

# Authentication & Security
Authentication: django-allauth >=65.0
Encryption: django-cryptography (TODO)
2FA: django-otp (TODO)

# Environment & Config
Environment: django-environ >=0.11
Settings: Split config (base/dev/staging/prod)

# Production
Deployment: Gunicorn >=22.0, WhiteNoise >=6.7
Monitoring: Sentry (TODO)
Caching: Redis (TODO)
Background Jobs: Celery (TODO)

# Development
Forms: django-crispy-forms >=2.3, crispy-tailwind >=1.0
Development: django-browser-reload >=1.15
Testing: pytest-django >=4.8, factory-boy >=3.3, coverage 87%
Code Quality: ruff, black, mypy (TODO)

# Assets
Media: Pillow >=10.4
Storage: S3 compatible (TODO)
```

### Project Architecture
- **Structure**: Enterprise-ready folder structure
- **Django Apps**:
  - `authentication` - Custom allauth integration
  - `users` - User management & profiles
  - `dashboard` - Main application interface
  - `backoffice` - Admin replacement (TODO)
- **Libraries**:
  - `libs/encryption` - GDPR-compliant field encryption (TODO)
  - `libs/security` - Middleware & decorators (TODO)
  - `libs/utils` - Shared utilities
- **Project Stage**: Foundation → Growth
- **Compliance**: GDPR-ready architecture

## Quick Start

### Creating Your First User Story

1. **Draft a story** in `.claude/scruaim/user-stories/draft/`:
   ```bash
   touch .claude/scruaim/user-stories/draft/US-001-user-profile-page.md
   ```

2. **Use the template** (see `user-stories/README.md`)

3. **Review** against `STORY-REVIEW.md` checklist

4. **Move to todo** when ready:
   ```bash
   mv .claude/scruaim/user-stories/draft/US-001-*.md .claude/scruaim/user-stories/todo/
   ```

## Workflow

### 1. Story Creation
```
draft/ → Review → todo/
```

### 2. Implementation
```
todo/ → In Progress → done/
```

### 3. Tracking (Optional)
- Update `backlog/in-progress.md` when starting
- Move to `backlog/completed.md` when done
- Capture lessons learned

## Django-Specific Patterns

### View Patterns
- **Class-based views**: Use `TemplateView`, `ListView`, `CreateView`
- **Login required**: Apply `LoginRequiredMixin` for protected views
- **Template naming**: `app_name/view_name.html`

### URL Patterns
```python
path('route/', ViewClass.as_view(), name='view-name'),
```

### App Structure
```
apps/app_name/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
├── models.py
├── templates/app_name/
├── tests/              # Enterprise test structure
│   ├── __init__.py
│   ├── factories.py
│   ├── test_models.py
│   └── test_views.py
├── urls.py
└── views.py
```

### Template Locations
- App templates: `apps/app_name/templates/app_name/`
- Global templates: `templates/`
- Static files: `static_src/` (development), `static/` (collected)

## Common Django Story Types

### 1. Model & Admin
```markdown
As a developer
I want to create a [Model] with admin interface
So that staff can manage [data] through Django admin
```

### 2. User-Facing View
```markdown
As a [user type]
I want to [view/create/update/delete] [resource]
So that I can [business value]
```

### 3. API Endpoint
```markdown
As an API consumer
I want to [GET/POST/PUT/DELETE] /api/[resource]/
So that I can [integrate/automate] [functionality]
```

### 4. Authentication Flow
```markdown
As a user
I want to [login/register/reset password]
So that I can access protected features
```

## Testing Approach

We use pytest with enterprise structure:
1. **Tests in `apps/*/tests/` folders** - organized by type
2. **Factory pattern** - Using factory-boy for test data
3. **Markers** - `@pytest.mark.unit`, `@pytest.mark.integration`
4. **Coverage target** - 70% minimum (currently 87%)
5. **Run tests** - `pytest` or `pytest apps/app_name/`

## Database Considerations

With PostgreSQL:
- Use appropriate field types (JSONField, ArrayField)
- Consider indexes for query optimization
- Plan migrations carefully
- Use transactions for data integrity

## Static Files & Tailwind

### Development
```bash
python manage.py tailwind start  # Watch mode
python manage.py tailwind build  # Production build
```

### In Templates
```django
{% load static %}
<link href="{% static 'css/styles.css' %}" rel="stylesheet">
```

## Authentication with Allauth

### Protected Views
```python
from django.contrib.auth.mixins import LoginRequiredMixin

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'protected.html'
```

### User Context
Available in templates as `{{ user }}`

## Quality Checklist

Before marking stories complete:
- [ ] Migrations created and applied
- [ ] Admin registered (if applicable)
- [ ] URLs configured
- [ ] Templates responsive (Tailwind)
- [ ] Forms use crispy-forms
- [ ] Static files collected
- [ ] Manual testing performed
- [ ] No Python errors
- [ ] No template errors

## Project-Specific Notes

1. **Testing Ready**: 60 tests written, 87% coverage achieved
2. **Four Apps**: `users`, `authentication`, `dashboard`, `core`
3. **Enterprise Structure**: Tests in `apps/*/tests/` folders
4. **Tailwind Integration**: Already configured, use utility classes
5. **Authentication Ready**: Allauth configured with email-based auth

## Getting Help

- **Django Docs**: Check Django 5.1 documentation
- **Pattern Questions**: Review existing views in `apps/`
- **Tailwind Classes**: Refer to Tailwind documentation
- **Database**: PostgreSQL-specific features available

## The One Rule

**Leave it better than you found it** - Every story should improve the codebase.