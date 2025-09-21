# US-001-security-configuration-fix

## Story
As a system administrator
I want to remove deprecated django-allauth settings and strengthen secret key validation
So that the application follows current security best practices and fails fast in production misconfigurations

## Context
The project currently uses deprecated django-allauth settings (ACCOUNT_AUTHENTICATION_METHOD, ACCOUNT_EMAIL_REQUIRED, ACCOUNT_USERNAME_REQUIRED) alongside their modern replacements. This creates deprecation warnings and potential confusion. Additionally, the SECRET_KEY configuration uses a weak fallback that could silently deploy to production without proper configuration.

**Current Issue**: Running `python manage.py check --deploy` shows deprecation warnings for allauth settings.

**Security Risk**: SECRET_KEY fallback allows production deployment without explicit key configuration.

## Acceptance Criteria
- [ ] No deprecation warnings when running `python manage.py check --deploy`
- [ ] SECRET_KEY validation prevents production deployment without explicit configuration
- [ ] All authentication functionality continues to work unchanged
- [ ] Development environment works with automatically generated dev key
- [ ] Modern allauth settings are preserved and functional

## Technical Approach

### Models Required
- [ ] No model changes needed

### Views & URLs
- [ ] No view/URL changes needed
- [ ] Authentication flow must remain functional

### Templates
- [ ] No template changes needed

### Forms (if applicable)
- [ ] No form changes needed

### Static Files
- [ ] No static file changes needed

## Implementation Checklist
- [ ] Remove deprecated ACCOUNT_EMAIL_REQUIRED from config/settings/base.py (line 151)
- [ ] Remove deprecated ACCOUNT_USERNAME_REQUIRED from config/settings/base.py (line 152)
- [ ] Remove deprecated ACCOUNT_AUTHENTICATION_METHOD from config/settings/base.py (line 153)
- [ ] Keep modern ACCOUNT_LOGIN_METHODS setting (line 154)
- [ ] Keep modern ACCOUNT_SIGNUP_FIELDS setting (line 155)
- [ ] Replace SECRET_KEY configuration with production-safe validation
- [ ] Add ImproperlyConfigured import
- [ ] Test authentication flow after changes
- [ ] Run Django checks to verify no warnings

## Test Requirements
```python
# Unit Tests (pytest-django)
class TestSecurityConfiguration:
    def test_allauth_settings_no_deprecation_warnings(self):
        # Run Django checks and verify no allauth deprecation warnings
        pass

    def test_secret_key_validation_development(self):
        # Verify dev environment works without SECRET_KEY env var
        pass

    def test_secret_key_validation_production(self):
        # Verify production settings raise error without SECRET_KEY
        pass

    def test_authentication_flow_unchanged(self, client):
        # Verify login/logout still works after settings changes
        pass
```

## Security Checklist
- [ ] SECRET_KEY validation prevents silent production misconfiguration
- [ ] No authentication functionality is broken
- [ ] Django security checks pass
- [ ] No sensitive information in fallback keys

## Manual Testing Steps
1. Remove SECRET_KEY from environment variables
2. Run `python manage.py runserver` - should work with dev key
3. Set DEBUG=False and test SECRET_KEY validation error
4. Test email login flow at `/auth/login/`
5. Test logout functionality
6. Run `python manage.py check --deploy` - verify no warnings
7. Verify user registration works
8. Check Django admin access (dev only)

## Performance Criteria
- [ ] No performance impact expected
- [ ] Authentication response times unchanged
- [ ] Django startup time unchanged

## Questions/Blockers
- None identified - straightforward configuration cleanup

## Definition of Done
- [ ] Code follows PRM standards
- [ ] No deprecation warnings in Django checks
- [ ] Security validation prevents production misconfig
- [ ] Authentication functionality verified working
- [ ] Manual testing passed
- [ ] Ready for code review

## Priority & Size
- Priority: High (Security configuration)
- Size: S (1-2 hours - configuration changes only)
- Sprint: Current

## Lessons Learned
[To be filled after implementation]

## Files to Modify
- `config/settings/base.py` - Remove deprecated settings, improve SECRET_KEY validation

## Current Settings (Before)
```python
# Lines 151-155 in config/settings/base.py
ACCOUNT_EMAIL_REQUIRED = True                    # DEPRECATED - Remove
ACCOUNT_USERNAME_REQUIRED = False               # DEPRECATED - Remove
ACCOUNT_AUTHENTICATION_METHOD = 'email'         # DEPRECATED - Remove
ACCOUNT_LOGIN_METHODS = {'email'}               # MODERN - Keep
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # MODERN - Keep

# Line 15 in config/settings/base.py
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')
```

## Expected Settings (After)
```python
# config/settings/base.py - Lines 151-153 REMOVED
# Keep only:
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

# Improved SECRET_KEY configuration:
from django.core.exceptions import ImproperlyConfigured

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY and not DEBUG:
    raise ImproperlyConfigured('SECRET_KEY must be set in production')
elif not SECRET_KEY:
    SECRET_KEY = 'django-insecure-dev-key-for-development-only'
```