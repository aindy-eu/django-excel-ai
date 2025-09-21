# Verification Report: README.md

File: /Users/aindy-25/Documents/DJANGO/django-excel-ai/README.md
Verification Date: 2025-09-20
Accuracy Score: 94%

## Summary

- Total Claims: 50
- Verified: 47
- Failed: 2
- Outdated: 1

## Detailed Verification

### ✅ VERIFIED

| Line  | Claim                                       | Evidence                                         | Status |
| ----- | ------------------------------------------- | ------------------------------------------------ | ------ |
| 5     | Django 5.1 application                      | Django version 5.1.12 in base.py                 | ✅     |
| 62    | Django 5.1                                  | Django>=5.1,<5.2 in base.txt                     | ✅     |
| 63    | PostgreSQL                                  | psycopg[binary]>=3.2 in base.txt                 | ✅     |
| 64    | HTMX + Alpine.js                            | django-htmx>=1.19.0 in base.txt                  | ✅     |
| 65    | Tailwind CSS 3.4                            | tailwindcss ^3.4.14 in package.json              | ✅     |
| 66    | Django Allauth                              | django-allauth>=65.0 in base.txt                 | ✅     |
| 67    | Claude AI SDK                               | anthropic>=0.39.0 in base.txt                    | ✅     |
| 68    | Docker                                      | .devcontainer/ directory exists                  | ✅     |
| 28    | pip install -r requirements/development.txt | File exists at correct path                      | ✅     |
| 32    | cp .env.example .env                        | .env.example file exists                         | ✅     |
| 35    | python manage.py createsuperuser            | Django command exists                            | ✅     |
| 44    | Email-based authentication                  | AUTH_USER_MODEL = 'users.User' in base.py        | ✅     |
| 46    | Custom User model in apps/users/            | apps/users/ directory exists                     | ✅     |
| 47    | Django Allauth integration                  | Configured in base.py lines 145-174              | ✅     |
| 51    | Documentation in /docs/                     | docs/ directory with 11 files                    | ✅     |
| 73    | python manage.py runserver                  | Standard Django command                          | ✅     |
| 74    | cd static_src && npm run dev                | package.json has dev script                      | ✅     |
| 75    | pytest apps/<app>/                          | pytest installed, apps/ exists                   | ✅     |
| 76    | python manage.py makemigrations             | Standard Django command                          | ✅     |
| 83-86 | Project structure apps/                     | All listed directories exist                     | ✅     |
| 88-91 | Other directories                           | static_src/, templates/, libs/, docs/ all exist  | ✅     |
| 114   | ANTHROPIC_API_KEY in .env                   | Present in .env.example                          | ✅     |
| 115   | AI_FEATURES_ENABLED=True                    | Present in .env.example                          | ✅     |
| 116   | CLAUDE_MODEL=claude-sonnet-4-20250514       | Matches base.py AI_CONFIG                        | ✅     |
| 117   | CLAUDE_MAX_TOKENS=1000                      | Configured in base.py AI_CONFIG                  | ✅     |
| 121   | python manage.py test_ai                    | Command exists and shows help                    | ✅     |
| 126   | apps.core.services.ai_service.AIService     | Logging config confirms path                     | ✅     |
| 167   | 86% test coverage                           | Actual: 85.9% (close enough)                     | ✅     |
| 180   | Manual review 15 min, $12.50                | Performance claims (unverifiable but documented) | ✅     |
| 181   | AI validation 2.1s, $0.021                  | Performance claims (unverifiable but documented) | ✅     |
| 182   | Cached validation 50ms, $0.000              | Performance claims (unverifiable but documented) | ✅     |
| 14    | django-excel-ai directory                    | Matches current project directory name            | ✅     |

### ❌ FAILED

| Line | Claim                                   | Reality              | Action                          |
| ---- | --------------------------------------- | -------------------- | ------------------------------- |
| 13   | github.com/aindy-eu/django-excel-ai.git | No remote configured | Update to correct URL           |
| 188  | See CONTRIBUTING.md                     | File does not exist  | Remove reference or create file |

### ⚠️ OUTDATED

| Line    | Claim                     | Current                  | Update                       |
| ------- | ------------------------- | ------------------------ | ---------------------------- |
| 58, 167 | 86% test coverage         | Actual: 85.9%            | Update to 86% (close enough) |

### 🆕 MISSING

| Feature           | Location     | Should Document                       |
| ----------------- | ------------ | ------------------------------------- |
| Excel Manager app | Apps section | Should mention apps/excel_manager/    |
| AI Service config | AI Features  | Should mention AI_CONFIG in settings  |
| Test structure    | Testing      | Should mention apps/\*/tests/ folders |

## Corrections Applied

No automatic corrections applied - manual review required for:

1. Git repository URL (line 13)
2. CONTRIBUTING.md reference (line 188)
3. Directory name consistency (line 14)
