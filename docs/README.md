# Project Documentation

## Overview
Enterprise-ready Django application with custom User model and Tailwind CSS.

## Documentation Structure

### Core Documentation
- [`project-structure.md`](./project-structure.md) - Complete file tree and project organization
- [`architecture.md`](./architecture.md) - Project structure and design decisions
- [`development.md`](./development.md) - Development setup and workflow
- [`technical.md`](./technical.md) - Technical specifications and configuration
- [`admin-strategy.md`](./admin-strategy.md) - Django admin patterns and customizations
- [`rails-to-django.md`](./rails-to-django.md) - Translation guide for Rails developers

### Directories
- [`claude-sdk/`](./claude-sdk/) - Claude AI SDK integration and features
- [`frontend/`](./frontend/) - Frontend documentation (Tailwind, JS, components)
- [`testing/`](./testing/) - Testing guidelines and strategies
- [`tools/`](./tools/) - Development tools and utilities

## Quick Links

### For Developers
- [Development Setup](./development.md#setup)
- [Running Tests](./testing/README.md)
- [Tailwind CSS Setup](./frontend/tailwind.md)

### For Architects
- [Directory Structure](./architecture.md#directory-structure)
- [Design Decisions](./architecture.md#design-decisions)
- [Technical Stack](./technical.md#stack)

## Project Status

### Core Infrastructure
- ✅ Custom User Model (email-based, no username field)
- ✅ Enterprise folder structure (`apps/`, `libs/`, `config/`)
- ✅ Environment-based settings (dev/test/prod)
- ✅ PostgreSQL database with optimized indexes
- ✅ Tailwind CSS 3.4 with PostCSS pipeline

### Completed Features
- ✅ **US-001**: Authentication app with Django Allauth integration
- ✅ **US-002**: Custom Allauth templates with Tailwind styling
- ✅ **US-003**: Email-based User model with extended UserProfile
- ✅ **US-005**: Avatar upload with drag-and-drop (HTMX + Alpine.js)
- ✅ **US-006**: Excel file upload and web-based display
- ✅ **US-007**: Claude AI SDK integration with service layer
- ✅ **US-008**: AI-powered Excel data validation with cost tracking

### TODO
- 📋 **US-004**: Security configuration hardening (deprecated settings removal)
- 📋 **US-042**: Fix deprecated Django Allauth settings (same as 004 but created with claude-opus-4-1-20250805)
- 📋 **US-009**: Admin consistency pattern
- 📋 **US-010**: CI/CD pipeline setup
- 📋 **US-011**: Explain SCRUAIM framework
- 📋 **US-012**: Explain AI handovers
- 📋 **US-013**: Explain slash commands

## For New Team Members

### Getting Started
1. **Setup:** Follow [Development Setup](./development.md#setup) - takes ~10 minutes
2. **Architecture:** Review [Directory Structure](./architecture.md#directory-structure) to understand the codebase
3. **Try the App:**
   - Login with email (no username required)
   - Upload an Excel file in Excel Manager
   - Test AI validation on your data

### Key Technical Decisions
- **Email-only authentication** - No username field, users login with email
- **HTMX for interactivity** - Server-side rendering with dynamic updates, no React/Vue needed
- **Service layer pattern** - Business logic in services, not views (see `apps/core/services/`)
- **Apps isolation** - Each app is self-contained with its own templates/tests

### Important Files
- **Settings:** `config/settings/` - Environment-based configuration
- **User Model:** `apps/users/models.py` - Custom email-based User
- **AI Service:** `apps/core/services/ai_service.py` - Claude integration
- **Main URLs:** `config/urls.py` - Root URL configuration

### Development Workflow
1. Create feature branch from `main`
2. Run tests: `pytest apps/<app_name>/`
3. Format code: `black apps/ && ruff check --fix apps/`
4. Commit with conventional format: `feat: description`

### User Story Locations
- **Completed:** `.claude/scruaim/user-stories/done/`
- **TODO:** `.claude/scruaim/user-stories/todo/`
- **Backlog:** `.claude/scruaim/user-stories/backlog/`