# User Stories Guide - Django Excel AI Validator

## Writing Effective User Stories

### Structure
- Use **specific verbs**: "upload", "delete", "view" instead of vague terms like "manage"
- Include **acceptance criteria** directly in the story
- Specify **technical constraints** upfront
- Reference **existing patterns** to follow (e.g., "like the email management feature")

### Improved Template
```markdown
US-XXX: [Specific Action] [Feature]
As a [user type]
I want to [specific action with details]
So that [clear business value]

Acceptance Criteria:
- [ ] Specific, measurable outcomes
- [ ] UI/UX requirements
- [ ] Error handling requirements
- [ ] Performance requirements

Technical Requirements:
- Framework/pattern to follow: [Reference existing example]
- Integration points: [List specific systems]
- Security considerations: [List specific concerns]

Out of Scope:
- [Related feature that won't be included]
- [Common request that's deferred]
```

## Naming Convention
All user stories must follow the pattern: `US-XXX-feature-name.md`
- **US** = User Story (constant prefix)
- **XXX** = Three-digit number (001, 002, etc.)
- **feature-name** = Kebab-case description

Example: `US-001-authentication-app-setup.md`

## Story Template

```markdown
# US-[XXX]-[feature-name]

## Story
As a [user type]
I want to [action/feature]
So that [business value]

## Context
[Why this story? Background information, business context]

## Acceptance Criteria
- [ ] [Specific, measurable requirement]
- [ ] [User-visible behavior]
- [ ] [Edge case handling]
- [ ] [Performance requirement if applicable]

## Technical Approach

### Models Required
- [ ] Model: [ModelName] with fields: [list fields]
- [ ] Encryption needed for PII: Yes/No (which fields?)
- [ ] Admin registration needed: No (use backoffice views)
- [ ] Migrations: [describe changes]
- [ ] Audit trail: Yes/No (compliance requirement?)

### Views & URLs
- [ ] View type: [TemplateView/ListView/CreateView/etc]
- [ ] URL pattern: /[path]/
- [ ] Template: [app_name/template_name.html]
- [ ] Login required: Yes/No
- [ ] Permission class: [AllowAny/IsAuthenticated/Custom]
- [ ] Rate limiting: Yes/No (threshold?)

### Templates
- [ ] Extends: base.html / dashboard_base.html
- [ ] Blocks used: [content, extra_css, extra_js]
- [ ] Components needed: [forms, tables, cards]

### Forms (if applicable)
- [ ] Form class: [FormName]
- [ ] Fields: [list fields]
- [ ] Validation: [custom validation needs]
- [ ] Crispy forms: Yes

### Static Files
- [ ] Custom CSS needed: Yes/No
- [ ] JavaScript functionality: [describe if needed]
- [ ] Tailwind utilities sufficient: Yes/No

## Implementation Checklist
- [ ] Create/update models
- [ ] Create migrations
- [ ] Register in admin (if applicable)
- [ ] Create views
- [ ] Configure URLs
- [ ] Create templates
- [ ] Add forms (if applicable)
- [ ] Style with Tailwind
- [ ] Add to navigation
- [ ] Test manually

## Test Requirements
```python
# Unit Tests (pytest-django)
class Test[Feature]:
    def test_[scenario](self, db):
        # Test [expected behavior]
        assert ...

    def test_permission_denied(self, client):
        # Security: Unauthorized access returns 403/redirect
        pass

    def test_data_encryption(self, user):
        # GDPR: PII fields are encrypted in DB
        pass
```

## Security Checklist
- [ ] No sensitive data in logs
- [ ] PII fields encrypted
- [ ] Rate limiting configured
- [ ] CSRF protection enabled
- [ ] SQL injection prevention verified

## Manual Testing Steps
1. [Step-by-step testing instructions]
2. [Include different user roles if applicable]
3. [Test edge cases]
4. [Check responsive design]
5. Security Testing:
   - [ ] Try accessing without login
   - [ ] Test with expired session
   - [ ] Verify no sensitive data in HTML/JS
   - [ ] Check browser console for errors/leaks

## Performance Criteria
- [ ] Page load < 2s
- [ ] Database queries < 10 per page
- [ ] No N+1 query problems
- [ ] Pagination for lists > 20 items

## Questions/Blockers
- [Any unknowns or dependencies]

## Definition of Done
- [ ] Code follows PRM standards
- [ ] No code duplication (2+ = extract)
- [ ] Security checklist complete
- [ ] Manual testing passed
- [ ] Performance criteria met
- [ ] Ready for code review

## Priority & Size
- Priority: [Critical/High/Medium/Low]
- Size: [S: 1-2h / M: 2-4h / L: 4-8h / XL: break down]
- Sprint: [Current/Next/Backlog]

## Lessons Learned
[To be filled after implementation]
```

## Django-Specific Story Guidelines

### 1. Model Stories
Always specify:
- Field types with Django field classes
- Relationships (ForeignKey, ManyToMany)
- Model methods needed
- Admin configuration
- Database indexes if needed

### 2. View Stories
Clarify:
- CBV (Class-Based View) or FBV (Function-Based View)
- Mixins needed (LoginRequiredMixin, PermissionRequiredMixin)
- Context data requirements
- Template inheritance structure

### 3. Form Stories
Include:
- Model forms vs regular forms
- Field widgets
- Validation logic
- Crispy forms layout
- CSRF handling

### 4. API Stories (if using DRF)
Define:
- Serializers needed
- ViewSets vs APIViews
- Authentication/permissions
- Pagination
- Filtering/searching

## Story Sizing Guide

### Small (1-2 hours)
- Single model with basic admin
- Simple template view
- Basic form
- CSS adjustments

### Medium (2-4 hours)
- Model with relationships
- ListView with filtering
- Form with validation
- Template with dynamic content
- Basic CRUD operations

### Large (4-8 hours)
- Multiple related models
- Complex business logic
- Multi-step forms
- Custom permissions
- API endpoints
- Extensive frontend work

### Extra Large (8+ hours)
- Should be broken down into smaller stories
- Consider creating an epic with sub-stories

## Common Patterns to Follow

### URL Naming
```python
app_name:view_name  # e.g., 'dashboard:profile'
```

### Template Structure
```django
{% extends "base.html" %}
{% load static %}
{% load crispy_forms_tags %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="container mx-auto px-4">
    <!-- Content here -->
</div>
{% endblock %}
```

### View Pattern
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class MyView(LoginRequiredMixin, TemplateView):
    template_name = 'app_name/my_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context
        return context
```

## Story Review Process

Before moving from `draft/` to `todo/`:

1. **Check completeness**: All sections filled
2. **Verify scope**: Story achievable in estimated time
3. **Dependencies clear**: No blockers identified
4. **Acceptance criteria**: Measurable and specific
5. **Technical approach**: Implementation path clear

## Anti-Patterns to Avoid

- ❌ **"Implement user management"** - Too vague, use specific actions like "view profile", "upload avatar", "change password"
- ❌ **"Make it work better"** - Not measurable, specify what "better" means
- ❌ **"Manage profile avatar"** - Ambiguous, use "upload avatar with drag-drop support"
- ❌ **Technical tasks disguised as user stories** - "Refactor database" is not a user story
- ❌ **Multiple features in one story** - Split into smaller, focused stories
- ❌ **Missing acceptance criteria** - How do you know when it's done?
- ❌ **No clear business value** - If you can't explain why, reconsider the story
- ❌ **Missing technical requirements** - Leads to implementation debates
- ❌ **No "Out of Scope" section** - Scope creep prevention is crucial

## Good Story Examples

### Example 1: Avatar Upload (Specific & Clear)
```markdown
US-005: Upload Profile Avatar with Drag-and-Drop

As a logged-in user
I want to upload a profile avatar using drag-and-drop or file selection
So that I can personalize my account with my photo

Acceptance Criteria:
- [ ] Support drag-and-drop onto upload area
- [ ] Support click-to-browse file selection
- [ ] Show image preview before upload
- [ ] Validate file size (max 5MB)
- [ ] Validate file type (JPG, PNG, WebP only)
- [ ] Display upload progress
- [ ] Auto-delete old avatar when uploading new one
- [ ] Show avatar with fallback to initials

Technical Requirements:
- Use HTMX patterns from email management feature
- Create Alpine.js component like dropdown.js
- Use Django signals for file cleanup
- Follow dark mode patterns

Out of Scope:
- Image cropping/editing
- Multiple avatar storage
- Social media import
```

### Example 2: User Profile View (Simple & Focused)
```markdown
As a logged-in user
I want to view my profile information
So that I can verify my account details are correct

Acceptance Criteria:
- [ ] Display full name, email, phone
- [ ] Show account status (active/verified)
- [ ] Display member since date
- [ ] Include edit profile button
```

### Example 3: Password Reset Flow
```markdown
As a user who forgot my password
I want to reset it via email verification
So that I can regain access to my account securely

Acceptance Criteria:
- [ ] Email sent within 30 seconds
- [ ] Link expires after 24 hours
- [ ] Password requirements shown
- [ ] Success confirmation displayed
```

## Remember

- **User-focused**: Write from the user's perspective
- **Value-driven**: Clear business value in "so that"
- **Testable**: Acceptance criteria must be verifiable
- **Sized right**: If it takes more than a day, break it down
- **Django-idiomatic**: Follow Django patterns and conventions