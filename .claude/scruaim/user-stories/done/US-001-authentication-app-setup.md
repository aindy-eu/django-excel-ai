# US-001-authentication-app-setup

## Story
As a developer
I want to set up a dedicated authentication app with proper folder structure
So that authentication is cleanly separated and enterprise-ready

## Context
Currently allauth is loosely integrated. We need a dedicated `apps/authentication/` app that owns all auth-related functionality, templates, and customizations. This follows enterprise patterns where authentication is a first-class citizen, not scattered across the codebase.

## Acceptance Criteria
- [ ] apps/authentication/ app created with proper structure
- [ ] allauth integrated through authentication app, not directly
- [ ] Custom templates structure ready for Tailwind styling
- [ ] Settings properly split (base/dev/prod)
- [ ] URLs routed through authentication app
- [ ] Dev admin works, prod admin disabled

## Technical Approach

### Models Required
- [ ] Model: None initially (using Django User)
- [ ] Encryption needed for PII: Future (profile data)
- [ ] Admin registration needed: Yes (dev only)
- [ ] Migrations: Initial app creation
- [ ] Audit trail: Yes (login/logout events)

### Views & URLs
- [ ] View type: Inherit from allauth views
- [ ] URL pattern: /auth/
- [ ] Template: apps/authentication/templates/account/
- [ ] Login required: No (public auth pages)
- [ ] Permission class: AllowAny
- [ ] Rate limiting: Yes (5 attempts/minute for login)

### Templates
- [ ] Extends: base.html (create if missing)
- [ ] Blocks used: [content, extra_css, extra_js]
- [ ] Components needed: [forms, error messages, success messages]

### Forms (if applicable)
- [ ] Form class: Extend allauth forms later
- [ ] Fields: Use allauth defaults initially
- [ ] Validation: Add rate limiting
- [ ] Crispy forms: Yes

### Static Files
- [ ] Custom CSS needed: No (Tailwind utilities)
- [ ] JavaScript functionality: Password visibility toggle
- [ ] Tailwind utilities sufficient: Yes

## Implementation Checklist
- [ ] Create apps/authentication/ directory structure
- [ ] Create apps.py with AppConfig
- [ ] Create adapters.py for allauth customization
- [ ] Create urls.py routing allauth.urls
- [ ] Create templates/account/ directory
- [ ] Create base template for auth pages
- [ ] Configure settings split (base/dev/prod)
- [ ] Update config/urls.py to include auth URLs
- [ ] Create initial migration
- [ ] Test login/logout flow
- [ ] Verify admin access in dev only

## Test Requirements
```python
# Unit Tests (pytest-django)
class TestAuthenticationSetup:
    def test_login_page_accessible(self, client):
        response = client.get('/auth/login/')
        assert response.status_code == 200

    def test_admin_disabled_in_prod(self, settings):
        settings.DEBUG = False
        # Verify admin returns 404
        pass

    def test_auth_urls_loaded(self):
        from django.urls import reverse
        assert reverse('account_login')
```

## Security Checklist
- [ ] No sensitive data in logs
- [ ] PII fields marked for future encryption
- [ ] Rate limiting configured on login
- [ ] CSRF protection enabled
- [ ] SQL injection prevention verified

## Manual Testing Steps
1. Navigate to /auth/login/
2. Verify page loads with proper template
3. Test login with invalid credentials (rate limiting)
4. Test login with valid credentials
5. Verify redirect to dashboard/home
6. Test logout functionality
7. Security Testing:
   - [ ] Try 6+ failed logins (rate limit kicks in)
   - [ ] Check HTML source for exposed data
   - [ ] Verify session cookie settings
   - [ ] Check browser console for errors

## Performance Criteria
- [ ] Page load < 2s
- [ ] Database queries < 5 per page
- [ ] No N+1 query problems
- [ ] Static files properly cached

## Questions/Blockers
- Need to decide on dashboard redirect URL
- Confirm rate limiting threshold (5/min?)

## Definition of Done
- [ ] Code follows PRM standards
- [ ] No code duplication (2+ = extract)
- [ ] Security checklist complete
- [ ] Manual testing passed
- [ ] Performance criteria met
- [ ] Ready for code review

## Priority & Size
- Priority: Critical (blocks all auth features)
- Size: M: 2-4h
- Sprint: Current