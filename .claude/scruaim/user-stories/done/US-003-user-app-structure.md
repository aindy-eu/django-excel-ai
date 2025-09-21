# US-003-user-app-structure

## Story
As a developer
I want to establish a proper users app with custom User model
So that user management is extensible and enterprise-ready from the start

## Context
Currently using default Django User. Need custom User model for future extensibility (additional fields, encryption, etc). This must be done BEFORE first migration to production. The users app will own all user-related functionality separate from authentication.

## Acceptance Criteria
- [ ] apps/users/ created with proper structure
- [ ] Custom User model extending AbstractUser
- [ ] Email as username (no separate username field)
- [ ] User profile model for extended data
- [ ] Proper model managers for common queries
- [ ] Admin registration (dev only)
- [ ] Future-proof for encryption/audit fields

## Technical Approach

### Models Required
- [ ] Model: User(AbstractUser) with email as USERNAME_FIELD
- [ ] Model: UserProfile with OneToOne to User
- [ ] Encryption needed for PII: Prepared (phone, address in profile)
- [ ] Admin registration needed: Yes (dev only, read-only prod)
- [ ] Migrations: Critical - must be done before any data
- [ ] Audit trail: Yes (created_at, updated_at, last_login)

### Views & URLs
- [ ] View type: None yet (model setup only)
- [ ] URL pattern: Future /users/profile/
- [ ] Template: Future
- [ ] Login required: N/A
- [ ] Permission class: N/A
- [ ] Rate limiting: N/A

### Templates
- [ ] None in this story (backend only)

### Forms (if applicable)
- [ ] Form class: Future UserProfileForm
- [ ] Fields: Future
- [ ] Validation: Future
- [ ] Crispy forms: Future

### Static Files
- [ ] None in this story

## Implementation Checklist
- [ ] Create apps/users/ directory
- [ ] Create custom User model
- [ ] Set USERNAME_FIELD = 'email'
- [ ] Remove username field
- [ ] Create UserProfile model
- [ ] Create UserManager with helper methods
- [ ] Update settings.AUTH_USER_MODEL
- [ ] Create initial migration
- [ ] Create admin.py with conditions
- [ ] Add signals for profile creation
- [ ] Create model tests
- [ ] Document future encryption fields

## Test Requirements
```python
# Unit Tests (pytest-django)
class TestUserModel:
    def test_user_creation_with_email(self, db):
        from apps.users.models import User
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        assert user.email == 'test@example.com'
        assert user.username == 'test@example.com'  # Should be same

    def test_profile_auto_created(self, db):
        from apps.users.models import User
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        assert hasattr(user, 'profile')
        assert user.profile is not None

    def test_manager_active_users(self, db):
        from apps.users.models import User
        active = User.objects.create_user(email='active@example.com')
        inactive = User.objects.create_user(email='inactive@example.com')
        inactive.is_active = False
        inactive.save()

        assert User.objects.active().count() == 1

    def test_future_encryption_fields(self, db):
        from apps.users.models import UserProfile
        # Ensure fields exist even if not encrypted yet
        profile = UserProfile()
        assert hasattr(profile, 'phone')
        assert hasattr(profile, 'address')
```

## Security Checklist
- [ ] Email field has unique constraint
- [ ] Password never stored in plain text
- [ ] PII fields identified for encryption
- [ ] No sensitive data in __str__ methods
- [ ] Audit fields non-editable

## Manual Testing Steps
1. Run migrations from scratch:
   ```bash
   rm -rf */migrations/
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Create superuser:
   ```bash
   python manage.py createsuperuser
   # Should ask for email, not username
   ```

3. Verify in shell:
   ```python
   from apps.users.models import User
   u = User.objects.first()
   assert u.profile is not None
   ```

4. Check admin (if DEBUG=True):
   - Navigate to /admin/
   - Verify User and UserProfile appear
   - Verify email is identifier

## Performance Criteria
- [ ] User queries optimized with select_related
- [ ] Profile access doesn't cause N+1
- [ ] Indexes on email field
- [ ] Manager methods use efficient queries

## Questions/Blockers
- Confirm email-only (no username) approach
- Which PII fields need encryption day-1?
- User deletion strategy (soft delete?)

## Definition of Done
- [ ] Code follows PRM standards
- [ ] No code duplication
- [ ] Security checklist complete
- [ ] Manual testing passed
- [ ] Performance criteria met
- [ ] AUTH_USER_MODEL configured
- [ ] Migration strategy documented

## Priority & Size
- Priority: Critical (MUST be before production)
- Size: M: 2-4h
- Sprint: Current

## ⚠️ CRITICAL WARNING
This MUST be completed before ANY production data exists. Changing AUTH_USER_MODEL after users exist is extremely difficult.