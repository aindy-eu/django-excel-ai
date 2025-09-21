# Handover: Enterprise Structure & Authentication Implementation - 20250915

## Context & Goals
- **What we were working on**: Transform Django project into enterprise-ready structure with custom User model
- **Why this matters**: Original project had default User, no clear structure, needed production-ready foundation
- **Key constraints**: Must implement custom User model before any production data exists
- **Success criteria**: Email-based auth working, clean enterprise structure, documentation in place

## Key Decisions Made

- **Custom User without username**: Chose email-only authentication because modern enterprise standard. Rejected username field completely to avoid confusion.

- **Hybrid apps/core + libs/ structure**: Kept `apps/core/` for Django utilities (following Two Scoops best practice) AND added `libs/` for pure Python utilities. Rejected putting everything in libs/ because core app is Django standard.

- **Keep allauth templates in account/**: Even though URLs are `/auth/`, templates stay in `account/` because allauth hardcodes this path. Rejected moving templates to avoid breaking allauth internals.

- **Nuclear database reset**: When faced with migration conflicts, chose complete DB drop/recreate. Rejected complex migration fixes because no production data existed yet.

- **No django-allauth-ui package**: Chose custom templates for full control. Rejected django-allauth-ui because it brings back widget_tweaks dependency we removed.

## Discoveries & Insights

- **allauth requires ACCOUNT_USER_MODEL_USERNAME_FIELD = None**: Not documented well - without this, signup fails with FieldDoesNotExist error for custom User without username.

- **Theme app was unused**: Found complete `theme/` Django app that wasn't in INSTALLED_APPS - leftover from initial setup. Safe to delete.

- **Empty apps (accounts, members)**: Multiple empty app directories created during exploration, causing confusion about structure.

- **URL namespace conflict**: allauth breaks if you add `app_name = 'authentication'` to its URL config - needs global namespace.

- **Settings deprecation warnings**: allauth v65+ deprecated several settings but still works with old names, just shows warnings.

## Current State

- **Completed**:
  - Custom User model with email as USERNAME_FIELD
  - Enterprise folder structure (apps/, libs/, docs/)
  - User Profile system with allauth integration
  - Documentation structure with proper separation
  - Template cleanup and organization
  - PostgreSQL database with fresh migrations

- **In Progress**:
  - Nothing actively in progress

- **Not Started**:
  - Styling remaining allauth templates (password change, email verify)
  - Writing tests for custom User model
  - Production security configuration

## Django-Specific Sections

### Database Schema Decisions
- **Custom User model**: Email as primary identifier, no username field at all
- **UserProfile**: Separate model with OneToOneField for extended data (future encryption)
- **UserManager**: Custom manager handling email-based user creation
- **Migration strategy**: Complete reset was safe pre-production

### Authentication & Security
- **allauth configuration**: ACCOUNT_USER_MODEL_USERNAME_FIELD = None critical for email-only
- **Admin access**: Only in DEBUG mode via settings check
- **Test credentials**: admin@example.com / admin123 for development

### URL Strategy
- `/auth/*` for all authentication (login, signup, password)
- `/dashboard/` for authenticated app area
- `/dashboard/profile/` for user settings
- `account` namespace kept global for allauth compatibility

### Performance Optimizations
- **None yet**: Focus was on correct structure first
- **Future**: select_related on User.profile queries identified as needed

## Next Steps (Priority Order)

1. **Immediate**: Style remaining allauth templates for consistency
2. **Next**: Write comprehensive tests for User model and auth flows
3. **Future**: Configure email backend for real verification emails

## What Files Don't Show

- **Why core AND libs**: Long discussion about Django best practices led to hybrid approach - Two Scoops recommends core app, but libs/ gives cleaner separation for non-Django code.

- **Initial confusion about account/ vs auth/**: Spent time trying to move allauth templates to match URL structure, but allauth expects account/ folder specifically.

- **TablePlus connection issue**: Database drop initially failed because TablePlus had active connection - user had to close it manually.

- **German mixed with English**: User switches between languages, started with German instructions then moved to English working mode.

## For Next AI/Human

- **Start here**: Check `/dashboard/profile/` to see working user profile system
- **Key context**: User model has NO username field - everything is email-based
- **Watch out for**: Don't try to move allauth templates from account/ folder
- **Testing login**: Use admin@example.com / admin123
- **PRM mode**: User frequently says "PRM" meaning Production Ready Mode - activate senior developer thinking

## Dead Ends Explored

- **Trying to namespace allauth URLs**: Adding app_name breaks URL reversing
- **Moving account/ templates**: allauth hardcodes these paths
- **Using widget_tweaks**: Removed in favor of crispy_forms only

## File Naming Conventions (User Preference)

- UPPERCASE only for: README, LICENSE, CHANGELOG
- Markdown files: use dashes not underscores (static-files-workflow.md ✅)
- Documentation: Split between CLAUDE.md (AI instructions) and docs/ (project docs)

## Session Achievements

- ✅ Custom User model implemented and working
- ✅ Enterprise structure with apps/core/libs separation
- ✅ Full user profile system with allauth integration
- ✅ Clean documentation structure
- ✅ Template organization following Django patterns
- ✅ PostgreSQL configured and migrated

---
*Session duration: ~3.5 hours*
*Context used: Heavy (multiple large file reads, parallel agents for analysis)*
*Key achievement: Complete transformation to enterprise-ready structure with custom auth*