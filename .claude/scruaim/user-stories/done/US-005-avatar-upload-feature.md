# US-005-avatar-upload-feature

## Story
As a logged-in user
I want to upload and manage my profile avatar
So that I can personalize my account and be easily identified in the application

## Context
Users currently have text initials as avatars. The `UserProfile` model already has an `avatar` ImageField (line 129-133 in models.py) but it's not exposed in the UI. This story adds upload functionality using HTMX for seamless updates and Alpine.js for interactive drag-and-drop, following existing patterns in the codebase.

## Acceptance Criteria
- [ ] Users can upload images (jpg, png, webp) up to 5MB
- [ ] Drag-and-drop zone with visual feedback
- [ ] Image preview before upload
- [ ] Old avatar automatically deleted when replaced
- [ ] Avatar displays in profile card instead of initials
- [ ] Graceful degradation without JavaScript
- [ ] Dark mode compatible UI
- [ ] Mobile responsive upload interface
- [ ] Success/error messages display correctly

## Technical Approach

### Models Required
- [ ] Model: UserProfile.avatar field EXISTS (apps/users/models.py:129-133)
- [ ] Add image validation in model clean method
- [ ] Migration: Not needed (field exists)
- [ ] Add method: `delete_old_avatar()` to cleanup files
- [ ] Signal: pre_save to delete old avatar file

### Views & URLs
- [ ] View: `AvatarUploadView` (HTMX-aware like `EmailManagementView`)
- [ ] URL: `/users/profile/avatar/` (add to apps/users/urls.py)
- [ ] Template: Extend existing profile.html
- [ ] Login required: Yes (LoginRequiredMixin)
- [ ] Method: POST only for upload
- [ ] Return: Partial template for HTMX

### Templates
- [ ] Create: `partials/htmx/_avatar_upload.html` (follow existing pattern)
- [ ] Update: `dashboard/partials/_profile_info_card.html` (show avatar)
- [ ] Add Alpine.js component for drag-drop (like existing dropdown.js)
- [ ] Use existing HTMX indicators and dark mode classes

### Forms
- [ ] Create: `AvatarUploadForm` in apps/users/forms.py
- [ ] Fields: avatar (ImageField)
- [ ] Validation: File size (5MB), type (image/*)
- [ ] Clean method: Verify image can be opened with Pillow
- [ ] Widget: Custom file input with Alpine.js data attributes

### Static Files
- [ ] Alpine component: `static/js/alpine/components/avatar-upload.js`
- [ ] No custom CSS (use existing Tailwind classes)
- [ ] Loading states use existing htmx-indicator pattern

## Implementation Checklist
- [ ] Extend ProfileUpdateForm to include avatar field
- [ ] Create HTMX view following EmailManagementView pattern
- [ ] Add URL pattern to users/urls.py
- [ ] Create partial template for upload zone
- [ ] Update profile info card to display avatar
- [ ] Add Alpine.js drag-drop component
- [ ] Configure media file serving (if not done)
- [ ] Add avatar cleanup on replacement
- [ ] Style with existing Tailwind utilities
- [ ] Test upload functionality

## Test Requirements
```python
# apps/users/tests/test_avatar_upload.py
import pytest
from apps.users.tests.factories import UserWithProfileFactory

@pytest.mark.integration
class TestAvatarUpload:
    def test_authenticated_upload_success(self, client, user_with_profile):
        """Test successful avatar upload for authenticated user."""
        # Upload valid image, assert success
        pass

    def test_file_size_limit_5mb(self, client, user_with_profile):
        """Test file size validation (5MB limit)."""
        # Upload >5MB file, assert rejection
        pass

    def test_invalid_file_type(self, client, user_with_profile):
        """Test file type validation."""
        # Upload .txt file, assert error
        pass

    def test_old_avatar_cleanup(self, client, user_with_profile):
        """Test old avatar is deleted when new one uploaded."""
        # Upload twice, assert first file deleted
        pass

    def test_htmx_partial_response(self, client, user_with_profile):
        """Test HTMX returns partial template."""
        # With HX-Request header, assert partial HTML
        pass

@pytest.mark.unit
@pytest.mark.auth
class TestAvatarSecurity:
    def test_malicious_file_rejection(self):
        """Test malicious files are rejected."""
        # PHP script as .jpg, assert rejected
        pass

    def test_unauthenticated_redirect(self, client):
        """Test unauthenticated users are redirected."""
        # No login, assert redirect to login
        pass
```

## Security Checklist
- [ ] File type validation (server-side)
- [ ] File size limits enforced
- [ ] No path traversal in filenames
- [ ] CSRF token required
- [ ] Login required for upload
- [ ] Validate image can be opened (not just extension)

## Manual Testing Steps
1. Login as test user (existing profile)
2. Navigate to /users/profile/
3. Click "Change Avatar" or drag image to drop zone
4. Verify preview displays
5. Submit upload, verify success message
6. Check avatar replaces initials in card
7. Upload new avatar, verify old one deleted
8. Test with 6MB file (should fail)
9. Test with .pdf file (should fail)
10. Toggle dark mode, verify UI consistency
11. Test on mobile viewport
12. Disable JavaScript, verify basic upload works

## Performance Criteria
- [ ] Image upload < 2s for 5MB file
- [ ] Preview generation < 100ms
- [ ] No N+1 queries on profile page
- [ ] Thumbnails generated on upload (150x150)

## Questions/Blockers
- Media files serving configured? (Check MEDIA_URL in urls.py)
- Need image optimization library? (Pillow installed)
- Maximum storage per user considerations?

## Definition of Done
- [ ] Code follows PRM standards (no duplication)
- [ ] HTMX/Alpine patterns match existing code
- [ ] All tests pass (70% coverage maintained)
- [ ] Manual testing completed
- [ ] Dark mode verified
- [ ] Old avatars cleaned up properly
- [ ] No console errors
- [ ] PR ready with tests

## Priority & Size
- Priority: Medium (enhances UX but not critical)
- Size: M (3-4 hours)
- Sprint: Current

## Implementation Notes for AIOC
**Key files to examine first:**
- `apps/users/models.py` - UserProfile.avatar field exists
- `apps/users/views.py` - EmailManagementView for HTMX pattern
- `apps/users/forms.py` - ProfileUpdateForm to extend
- `templates/partials/htmx/` - Existing HTMX partials
- `static/js/alpine/components/` - Alpine component patterns

**Media configuration check:**
```bash
grep -r "MEDIA_URL\|MEDIA_ROOT" config/
grep -r "static(settings.MEDIA_URL" config/urls.py
```

**Existing patterns to follow:**
1. HTMX views return partials when `request.htmx` is true
2. Alpine components are separate JS files in `static/js/alpine/components/`
3. Dark mode uses `dark:` prefix on Tailwind classes
4. Forms use ProfileUpdateForm as base (already has Tailwind styling)
5. Tests use pytest with existing factories

## Lessons Learned
[To be filled after implementation]