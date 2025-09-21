# Backlog - Django Excel AI Validator

> Current project state (Status Quo) - No future features or ideas

## Project Status Quo

### Core Features Implemented
- **Authentication System**: Email-based auth with django-allauth
- **User Management**: Custom user model with avatar support
- **Excel Processing**: Upload, display, and manage Excel files
- **AI Validation**: Claude API integration for Excel validation
- **Dashboard**: Basic dashboard interface with HTMX

### Current Todo Stories (In Repository)

#### 1. Security Configuration Fix
- **Story**: `user-stories/todo/US-004-security-configuration-fix.md`
- **Status**: Todo
- **Priority**: High (Security)
- **Description**: Fix security settings for production readiness

#### 2. Admin Consistency Pattern
- **Story**: `user-stories/todo/US-009-admin-consistency-pattern.md`
- **Status**: Todo
- **Priority**: Medium
- **Description**: Standardize admin interface patterns

#### 3. Fix Allauth Deprecated Settings
- **Story**: `user-stories/todo/US-042-fix-allauth-deprecated-settings.md`
- **Status**: Todo
- **Priority**: High (Technical Debt)
- **Description**: Update deprecated allauth settings

## System Architecture (Current State)

### Django Apps
1. **authentication** - Custom allauth integration
2. **core** - Shared services, AI integration
3. **dashboard** - Main user interface
4. **excel_manager** - Excel file processing & validation
5. **users** - User profiles and management

### Technology Stack (Deployed)
- Django 5.1+ framework
- PostgreSQL database
- HTMX for frontend interactivity (no React/Vue)
- Tailwind CSS for styling
- Anthropic Claude API for AI validation
- 86% test coverage with pytest

### Current Capabilities
- Users can register with email
- Users can upload Excel files
- System validates Excel with AI
- Files are tracked per user
- Dashboard shows user's files
- Admin interface available (DEBUG mode)

## No Future Features
Per instruction: This backlog contains only the current state (SQ) of the project. No future ideas or enhancements are tracked here.

---

*Last updated: 2025-09-20*
*Active todo stories: 3*
*Test coverage: 86%*