# Testing Guide - Enterprise Pytest Strategy

## Overview
Enterprise-ready testing with pytest for Django 5.1 applications.

## Test Structure

```
.
├── pytest.ini              # Pytest configuration
├── conftest.py            # Root fixtures
└── apps/
    ├── users/tests/
    │   ├── factories.py        # User factories
    │   ├── test_models.py      # Model tests
    │   ├── test_views.py       # Profile view tests
    │   └── test_avatar_upload.py # Avatar upload tests
    ├── authentication/tests/
    │   └── test_auth.py        # Auth flow tests
    ├── dashboard/tests/
    │   └── test_views.py       # Dashboard view tests
    ├── core/tests/
    │   └── test_ai_service.py  # AI service tests
    └── excel_manager/tests/
        ├── conftest.py         # Excel-specific fixtures
        └── test_ai_validation.py # AI validation tests
```

## Running Tests

### All Tests
```bash
pytest
```

### Specific App
```bash
pytest apps/users
pytest apps/authentication
pytest apps/dashboard
pytest apps/excel_manager

# Note: Running app-specific tests only measures coverage for that app's code
# For full coverage report, run all tests with: pytest apps/
```

### Specific Test File
```bash
pytest apps/users/test_models.py
```

### With Coverage
```bash
pytest --cov=apps --cov-report=html
# Open htmlcov/index.html to view report
```

### By Markers
```bash
pytest -m unit          # Fast unit tests
pytest -m integration   # Integration tests
pytest -m auth         # Authentication tests
pytest -m "not slow"   # Skip slow tests
```

### Parallel Execution
```bash
pytest -n auto  # Auto-detect CPU cores
pytest -n 4     # Use 4 processes
```

## Test Types

### Unit Tests
Test individual functions and methods in isolation.

```python
import pytest
from apps.users.models import User

@pytest.mark.unit
@pytest.mark.model
def test_create_user_with_email(db):
    user = User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )
    assert user.email == 'test@example.com'
    with pytest.raises(AttributeError):
        _ = user.username  # No username field
```

### Integration Tests
Test interaction between components.

```python
import pytest
from django.urls import reverse
from apps.users.factories import UserFactory

@pytest.mark.integration
@pytest.mark.auth
def test_login_flow(client, db):
    user = UserFactory(email='test@example.com', password='testpass123')

    response = client.post(reverse('account_login'), {
        'login': 'test@example.com',
        'password': 'testpass123'
    })

    assert response.status_code == 302
    assert response.url == '/dashboard/'
```

### View Tests
Test Django views and templates.

```python
import pytest
from django.urls import reverse

@pytest.mark.view
@pytest.mark.integration
def test_dashboard_requires_login(client):
    response = client.get(reverse('dashboard:index'))
    assert response.status_code == 302
    assert '/auth/login/' in response.url
```

## Fixtures & Factories

### Built-in Fixtures (conftest.py)
```python
# Available fixtures:
client              # Django test client
user                # Standard test user
admin_user          # Admin test user
authenticated_client # Client with logged-in user
admin_client        # Client with logged-in admin
user_factory        # Factory function for users
api_client          # API test client
cleanup_test_media  # Auto-cleanup test files
```

### Factory Pattern
```python
# apps/users/factories.py
from apps.users.factories import UserFactory, UserWithProfileFactory

# Usage in tests
@pytest.fixture
def custom_user():
    return UserFactory(
        email='custom@example.com',
        first_name='John',
        is_verified=True
    )

def test_something(custom_user):
    assert custom_user.is_verified is True
```

## Testing Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Names**: Test names should describe what they test
3. **AAA Pattern**: Arrange, Act, Assert
4. **Use Markers**: Categorize tests for selective execution
5. **Test Edge Cases**: Empty data, invalid input, boundaries
6. **Keep Tests Fast**: Use `--reuse-db`, avoid sleep()

## Pytest Configuration (pytest.ini)

```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
testpaths = apps
addopts =
    --reuse-db           # Reuse test database
    --nomigrations       # Skip migrations
    --cov=apps           # Coverage for apps
    --cov-fail-under=70  # Minimum 70% coverage
markers =
    unit: Unit tests
    integration: Integration tests
    auth: Authentication tests
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.13
      - name: Install dependencies
        run: |
          pip install -r requirements/test.txt
      - name: Run tests
        run: |
          pytest --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Test Coverage Goals

- **Phase 1**: 70% overall (current target)
- **Phase 2**: 85% for critical paths
- **Phase 3**: 100% for authentication

## Test Suite Statistics

- **Total Test Files**: 9 test files across 5 apps
- **Test Count**: ~120 tests
- **Coverage**: 70% minimum enforced
- **Apps with Tests**: users, authentication, dashboard, core, excel_manager

## Common Test Patterns

### Testing Email Authentication
```python
@pytest.mark.auth
class TestEmailAuth:
    def test_no_username_field(self, user):
        """Ensure User model has no username field"""
        with pytest.raises(AttributeError):
            _ = user.username

    def test_email_is_username(self, db):
        """Email is the USERNAME_FIELD"""
        assert User.USERNAME_FIELD == 'email'
```

### Testing Protected Views
```python
@pytest.mark.integration
def test_protected_view(client, authenticated_client):
    """Test login required decorator"""
    # Anonymous - should redirect
    response = client.get('/dashboard/')
    assert response.status_code == 302

    # Authenticated - should work
    response = authenticated_client.get('/dashboard/')
    assert response.status_code == 200
```

### Using Factories
```python
def test_batch_users(db):
    """Create multiple test users"""
    users = UserFactory.create_batch(10)
    assert User.objects.count() == 10
    assert all(u.email for u in users)
```