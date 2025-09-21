# Admin Strategy: Dev vs Production

## Philosophy
Django Admin is a **development tool**, not a production interface. Use it wisely.

## Current Implementation Status

### Development Environment
```python
# settings/development.py
DEBUG = True
ADMIN_ENABLED = True
```
- Full Django Admin access for rapid development
- Models registered conditionally based on settings
- Admin URL available at `/admin/`

### Production Environment
```python
# settings/production.py
DEBUG = False
ADMIN_ENABLED = False  # Or use environment variable for emergency access
# ADMIN_ENABLED = os.environ.get('EMERGENCY_ADMIN', 'False') == 'True'
```
- Admin access disabled by default
- Emergency access possible via environment variable
- **Note**: Backoffice app not yet implemented (planned for future)

## Admin Registration Pattern

### Currently Implemented Pattern
```python
# apps/[app]/admin.py
from django.contrib import admin
from django.conf import settings
from .models import MyModel

# Most apps use this pattern (users, authentication):
if settings.DEBUG or getattr(settings, 'ADMIN_ENABLED', False):
    @admin.register(MyModel)
    class MyModelAdmin(admin.ModelAdmin):
        list_display = ['field1', 'field2', 'created_at']
        readonly_fields = ['sensitive_field']  # Never editable

# Note: excel_manager currently uses simplified pattern:
if settings.DEBUG:
    # Registration here
```

### Actual Implementations
- **Users app**: ✅ Full pattern with email-based User model, GDPR awareness
- **Excel Manager**: ⚠️ Only checks DEBUG (should be updated for consistency)
- **Authentication**: ✅ Follows pattern (placeholder for future models)
- **Dashboard**: ✅ Empty admin.py (no models registered yet)
- **Core**: No admin.py file (no models to register)

## Backoffice App (Future Implementation)

**Status**: Not yet implemented. This is a planned feature for production use.

```python
# Future: apps/backoffice/views.py
class BackofficeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Read-only view for staff to review data"""

    def test_func(self):
        if settings.DEBUG:
            return self.request.user.is_staff
        return self.request.user.groups.filter(name='backoffice').exists()
```

## Security Rules

1. **Never expose admin in production** without extreme measures
2. **Readonly by default** - even in dev for sensitive fields
3. **Audit everything** - log all admin/backoffice actions
4. **Use groups/permissions** - not is_staff/is_superuser in production
5. **2FA required** for any production admin/backoffice access

## Migration Path

### Current Status: Phase 1
- ✅ Django Admin enabled in development
- ✅ Disabled in production (with emergency override option)
- ✅ Conditional registration based on settings

### Next Steps:
1. **Phase 2**: Build basic backoffice views for common tasks (not started)
2. **Phase 3**: Gradually move all admin functionality to backoffice
3. **Phase 4**: Admin becomes emergency-only tool

### Next Steps:
- [ ] Consider implementing basic backoffice app for production use

## Emergency Admin Access (Break Glass)

```python
# settings/prod.py
import os
from datetime import datetime

# Emergency admin activation
if os.getenv('EMERGENCY_ADMIN_UNTIL'):
    emergency_until = datetime.fromisoformat(os.getenv('EMERGENCY_ADMIN_UNTIL'))
    if datetime.now() < emergency_until:
        ADMIN_ENABLED = True
        ADMIN_URL = os.getenv('EMERGENCY_ADMIN_URL')  # Random URL
        # Alert security team
        import logging
        logging.critical(f"EMERGENCY ADMIN ACTIVE UNTIL {emergency_until}")
```

This ensures admin is a tool, not a crutch.

## Key Findings from Code Review

### What's Actually Implemented:
- ✅ Admin URL conditionally added based on `DEBUG or ADMIN_ENABLED` in `config/urls.py` (line 32-33)
- ✅ Email-based User model properly configured (no username)
- ✅ GDPR-aware admin with PII sections marked in users app
- ✅ Readonly fields for sensitive data
- ✅ Production settings with ADMIN_ENABLED = False
- ❌ Backoffice app does not exist yet (planned feature)

### Documentation vs Reality:
- Most documentation accurately reflects the **intended** architecture
- Implementation is partially complete (Phase 1 of 4)
- Emergency admin access pattern is simplified in actual settings (basic override without datetime checks)

---
*Last verified against codebase: 2025-09-19*