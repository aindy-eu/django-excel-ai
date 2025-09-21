# US-002-allauth-custom-templates

## Story
As a user
I want to see professional, branded authentication pages
So that I trust the application and have a seamless experience

## Context
Default allauth templates look like 1990s web forms. We need modern, Tailwind-styled templates that match our brand and provide excellent UX. No django-allauth-ui package - we build our own for full control.

## Acceptance Criteria
- [ ] Login page with modern design and branding
- [ ] Signup page with clear value proposition
- [ ] Password reset flow with user-friendly messaging
- [ ] Email confirmation pages styled consistently
- [ ] Logout confirmation (if needed) or direct logout
- [ ] Error states clearly communicated
- [ ] Success messages properly styled
- [ ] Mobile-responsive on all auth pages

## Technical Approach

### Models Required
- [ ] Model: None (template-only story)
- [ ] Encryption needed for PII: N/A
- [ ] Admin registration needed: N/A
- [ ] Migrations: None
- [ ] Audit trail: Use existing

### Views & URLs
- [ ] View type: Override allauth templates only
- [ ] URL pattern: /auth/* (existing)
- [ ] Template: apps/authentication/templates/account/*.html
- [ ] Login required: Varies by page
- [ ] Permission class: AllowAny for public pages
- [ ] Rate limiting: Inherited from 001

### Templates
- [ ] Extends: authentication/base_auth.html
- [ ] Blocks used: [auth_content, auth_title, auth_scripts]
- [ ] Components needed: [form inputs, buttons, alerts, cards]

### Forms (if applicable)
- [ ] Form class: Use allauth forms with widget_tweaks
- [ ] Fields: Styled with Tailwind classes
- [ ] Validation: Display inline errors
- [ ] Crispy forms: Optional (widget_tweaks preferred)

### Static Files
- [ ] Custom CSS needed: Minimal (auth-specific utilities)
- [ ] JavaScript functionality: Show/hide password, form validation
- [ ] Tailwind utilities sufficient: 95% (custom for animations)

## Implementation Checklist
- [ ] Create base_auth.html template
- [ ] Create login.html with Tailwind styling
- [ ] Create signup.html with password requirements
- [ ] Create password_reset.html flow (4 templates)
- [ ] Create email/ templates for confirmations
- [ ] Create logout.html (or configure direct logout)
- [ ] Add password visibility toggle JS
- [ ] Add client-side validation helpers
- [ ] Create email templates (HTML + text)
- [ ] Add loading states for form submissions
- [ ] Test all flows end-to-end
- [ ] Verify mobile responsiveness

## Test Requirements
```python
# Unit Tests (pytest-django)
class TestAuthTemplates:
    def test_login_template_used(self, client):
        response = client.get('/auth/login/')
        assert 'authentication/base_auth.html' in [t.name for t in response.templates]

    def test_tailwind_classes_present(self, client):
        response = client.get('/auth/login/')
        assert 'bg-white shadow rounded-lg' in response.content.decode()

    def test_password_toggle_script(self, client):
        response = client.get('/auth/login/')
        assert 'togglePassword' in response.content.decode()

    def test_mobile_viewport(self, client):
        response = client.get('/auth/login/')
        assert 'viewport' in response.content.decode()
```

## Security Checklist
- [ ] No passwords in HTML comments
- [ ] CSRF tokens on all forms
- [ ] No sensitive data in client-side JS
- [ ] Secure password requirements shown
- [ ] No autocomplete on sensitive fields

## Manual Testing Steps
1. Test Login Flow:
   - Load /auth/login/
   - Verify professional appearance
   - Test show/hide password
   - Submit with invalid credentials
   - Verify error styling
   - Submit with valid credentials
   - Verify redirect

2. Test Signup Flow:
   - Load /auth/signup/
   - Verify password requirements shown
   - Test weak password rejection
   - Complete valid signup
   - Verify email sent

3. Test Password Reset:
   - Full flow from request to reset
   - Verify all 4 pages styled

4. Mobile Testing:
   - Test all pages on mobile viewport
   - Verify touch-friendly buttons
   - Check form usability

## Performance Criteria
- [ ] Page load < 1s (templates only)
- [ ] Minimal JavaScript (<10KB)
- [ ] CSS purged of unused Tailwind
- [ ] Images optimized (<100KB total)

## Questions/Blockers
- Brand colors/logo needed?
- Password complexity requirements?
- Social login templates (future)?

## Definition of Done
- [ ] Code follows PRM standards
- [ ] No code duplication in templates
- [ ] Security checklist complete
- [ ] Manual testing passed
- [ ] Performance criteria met
- [ ] Matches design system (when defined)

## Priority & Size
- Priority: Critical (UX/trust)
- Size: M: 2-4h
- Sprint: Current