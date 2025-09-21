# US-042-fix-allauth-deprecated-settings

## Story
As a Django developer
I want to update deprecated django-allauth settings to current standards
So that the application avoids deprecation warnings and follows 2024-2025 best practices

## Context
Django-allauth 65.x has deprecated several authentication settings. Running `python manage.py check --deploy` shows three deprecation warnings:
- `ACCOUNT_AUTHENTICATION_METHOD` is deprecated → use `ACCOUNT_LOGIN_METHODS`
- `ACCOUNT_EMAIL_REQUIRED` is deprecated → use `ACCOUNT_SIGNUP_FIELDS`
- `ACCOUNT_USERNAME_REQUIRED` is deprecated → use `ACCOUNT_SIGNUP_FIELDS`

This technical debt should be resolved to maintain code quality and prepare for future django-allauth versions where these settings may be removed entirely.

## Acceptance Criteria
- [ ] No deprecation warnings from django-allauth when running `python manage.py check --deploy`
- [ ] Authentication still works with email-only login (no username field)
- [ ] All existing authentication flows remain functional
- [ ] Settings follow django-allauth 65.x conventions
- [ ] Optional: Add missing `SECURE_REFERRER_POLICY` security header

## Technical Approach

### Models Required
- [ ] Model: None (settings change only)
- [ ] Encryption needed for PII: N/A
- [ ] Admin registration needed: N/A
- [ ] Migrations: None required
- [ ] Audit trail: No

### Views & URLs
- [ ] View type: N/A (configuration change)
- [ ] URL pattern: N/A
- [ ] Template: N/A
- [ ] Login required: N/A
- [ ] Permission class: N/A
- [ ] Rate limiting: N/A

### Templates
- [ ] No template changes required

### Forms (if applicable)
- [ ] N/A

### Static Files
- [ ] Custom CSS needed: No
- [ ] JavaScript functionality: No
- [ ] Tailwind utilities sufficient: N/A

## Implementation Checklist
- [ ] Open `config/settings/base.py`
- [ ] Remove deprecated settings (lines 151-153):
  - [ ] Delete line 151: `ACCOUNT_EMAIL_REQUIRED = True`
  - [ ] Delete line 152: `ACCOUNT_USERNAME_REQUIRED = False`
  - [ ] Delete line 153: `ACCOUNT_AUTHENTICATION_METHOD = 'email'` (optional - redundant)
- [ ] Verify modern settings remain (lines 154-155):
  - [ ] `ACCOUNT_LOGIN_METHODS = {'email'}`
  - [ ] `ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']`
- [ ] Optional: Add to `config/settings/production.py` after line 27:
  - [ ] `SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'`
- [ ] Run `python manage.py check --deploy` to verify warnings resolved
- [ ] Test authentication flows manually

## Test Requirements
```python
# Quick verification in Django shell
python manage.py shell
>>> from django.conf import settings
>>> assert settings.ACCOUNT_LOGIN_METHODS == {'email'}
>>> assert settings.ACCOUNT_SIGNUP_FIELDS == ['email*', 'password1*', 'password2*']
>>> assert not hasattr(settings, 'ACCOUNT_EMAIL_REQUIRED')
>>> assert not hasattr(settings, 'ACCOUNT_USERNAME_REQUIRED')

# Run deployment check
python manage.py check --deploy 2>&1 | grep -i "deprecat"
# Should return no django-allauth deprecation warnings

# Optional: pytest test
import pytest
from django.core.management import call_command
from io import StringIO

@pytest.mark.django_db
def test_no_allauth_deprecation_warnings():
    """Verify no django-allauth deprecation warnings."""
    out = StringIO()
    call_command('check', '--deploy', stdout=out)
    output = out.getvalue()
    assert 'ACCOUNT_AUTHENTICATION_METHOD is deprecated' not in output
    assert 'ACCOUNT_EMAIL_REQUIRED is deprecated' not in output
    assert 'ACCOUNT_USERNAME_REQUIRED is deprecated' not in output
```

## Security Checklist
- [ ] No sensitive data exposed in settings
- [ ] Authentication configuration remains secure
- [ ] Email-only authentication still enforced
- [ ] CSRF protection unaffected
- [ ] Optional: `SECURE_REFERRER_POLICY` added for additional security

## Manual Testing Steps
1. Run `python manage.py check --deploy` - verify no allauth warnings
2. Start development server: `python manage.py runserver`
3. Test login flow at `/auth/login/`:
   - [ ] Email field present
   - [ ] No username field
   - [ ] Can login with test account
4. Test signup flow at `/auth/signup/`:
   - [ ] Only email and password fields shown
   - [ ] No username field requested
   - [ ] Can create new account
5. Test logout at `/auth/logout/`
6. Verify admin login still works at `/admin/`

## Performance Criteria
- [ ] No performance impact (configuration change only)

## Questions/Blockers
- None identified - deprecation warnings are clear and replacements documented

## Definition of Done
- [ ] Code follows PRM standards
- [ ] No code duplication (settings already exist, just removing deprecated ones)
- [ ] Security checklist complete
- [ ] Manual testing passed
- [ ] Performance criteria met (no impact)
- [ ] Ready for code review

## Priority & Size
- Priority: High (deprecation warnings in production logs)
- Size: S (15 minutes)
- Sprint: Current (technical debt cleanup)

## Lessons Learned
[To be filled after implementation]
- Running `python manage.py check --deploy` is valuable for catching deprecation warnings
- Django-allauth migrations from single settings to set-based configuration allow more flexibility
- Always verify authentication flows after configuration changes