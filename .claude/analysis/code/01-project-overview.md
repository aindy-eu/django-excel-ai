# Project Overview - Code Analysis

## Project Identity (From Code)

**Project Type**: Django Web Application with AI-Enhanced Excel Processing
**Primary Language**: Python (5,839 files found)
**Framework**: Django 5.1+ with HTMX for frontend interactivity

## Purpose (Inferred from Implementation)

Based on code analysis, this is an Excel file validation and management system that:

1. **Processes Excel Files**: Found `ExcelUploadView`, `ExcelDetailView` classes in `excel_manager` app
2. **AI-Powered Validation**: `ValidateWithAIView` class uses Anthropic API for Excel validation
3. **User Management**: Custom user model with email-based authentication (no username field)
4. **Dashboard Interface**: Dashboard app with template views for data visualization

## Target Users (From Functionality)

- Business analysts uploading Excel files for validation
- Data teams needing AI-assisted data quality checks
- Organizations requiring structured Excel file management

## Actual Metrics

```bash
# File counts
Total Python files: 5,839
Application code (./apps): 64 files
Test files collected: 120

# Test coverage
Overall coverage: 86% (1848 statements, 260 not covered)
Test framework: pytest with coverage reporting

# Codebase size
Apps implemented: 5
- authentication (custom auth flows)
- core (shared services, AI integration)
- dashboard (main interface)
- excel_manager (file processing)
- users (user management)

# Repository activity
Last commit: 2025-09-20 10:54:57 +0200
Active development: Yes
```

## Core Business Logic (From Code)

### Excel Processing Pipeline
1. User uploads Excel file (`ExcelUploadView`)
2. File stored and tracked in database (`excel_manager/models.py`)
3. AI validation available on-demand (`ValidateWithAIView`)
4. Results displayed in detail view (`ExcelDetailView`)
5. Files can be deleted (`DeleteExcelView`)

### AI Integration
- Service layer: `apps.core.services.ai_service.AIService`
- Provider: Anthropic API (Claude)
- Purpose: Excel data validation and quality checks
- Management command: Available for batch processing

### Authentication System
- Email-based login (no usernames)
- Django-allauth integration
- Custom user model with profile support
- Login required for all Excel operations

## Problem Solved

This application addresses the need for:
1. **Automated Excel validation** - Using AI to detect data quality issues
2. **Centralized file management** - Track and manage Excel uploads
3. **User accountability** - All operations tied to authenticated users
4. **Structured workflow** - Clear upload → validate → review process

## Technology Choices (From Imports)

```python
# Core dependencies found
Django >= 5.1          # Modern Django
django-allauth >= 65.0 # Authentication
django-htmx >= 1.19.0  # Interactive UI without JavaScript frameworks
Anthropic API          # AI validation
psycopg[binary]        # PostgreSQL database
Pillow                 # Image processing
openpyxl               # Excel file handling
```

## Application Scale

- **Monolithic architecture**: Single Django project with multiple apps
- **Traditional MVC**: Views, models, templates structure
- **Server-rendered**: HTMX for interactivity, no SPA framework
- **Database-driven**: PostgreSQL with Django ORM
- **Test-driven**: 86% coverage with comprehensive test suite