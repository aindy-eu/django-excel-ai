# Claude AI Assistant Instructions

## Project Context

**Django Excel AI Validator** - A production-ready Django 5.1 application with:
- Enterprise Django patterns with clean architecture
- HTMX + Alpine.js for hypermedia-driven development (no React/Vue)
- AI-powered Excel validation using Claude Sonnet 4
- Custom email-based authentication (no username field)
- Comprehensive pytest test suite with factories and fixtures

## Core Principles

### 🤖 Parallel Agent Strategy
When facing tasks that involve checking/analyzing multiple items (packages, files, patterns):
- **Use parallel agents** when you have 5+ items to check
- **Split work evenly** across 2-4 agents based on volume
- **Good for:** Package usage checks, file pattern searches, multi-file refactoring analysis
- **Example:** Checking 39 packages? Use 3 agents with ~13 packages each

When modifying multiple similar files:
- **Use parallel agents** for independent file modifications
- **Perfect for:** Locale files, test files, similar config files
- **Example:** Updating en.json and de.json? Use 2 agents to update both simultaneously

This dramatically speeds up analysis and provides results faster.

### 🧠 Production Ready Mode (PRM)
When I say "PRM", activate senior developer thinking:

@~/.claude/partials/prm-core.md

#### Key Development Rules
1. **NEVER auto-commit changes** - only commit when explicitly requested with "commit", "git commit", or similar explicit commands
2. **NEVER delete feature branches** after merging
3. **Always verify changes** with pytest and code quality tools before marking complete

## 📅 Date Formatting
**For filenames and technical identifiers**, use the compact format: `YYYYMMDD`
- Check the current date in the shell ```date +%Y%m%d```
- ⚠️ **Filenames**: Use `20250915`, not `2025-09-15` (dashes break sorting)
- ✅ **In documentation text**: ISO format `2025-09-15` is fine for readability

## Important Conventions

### Commit Messages
Use **Conventional Commits** format: `type(scope): description`

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code change that neither fixes a bug nor adds a feature
- `test:` Adding or updating tests
- `chore:` Maintenance tasks, dependency updates
- `perf:` Performance improvements
- `ci:` CI/CD changes

**Optional Scopes** (use when applicable):
- `(auth)` - Authentication/authorization
- `(excel)` - Excel manager app
- `(dashboard)` - Dashboard app
- `(users)` - Users app
- `(core)` - Core utilities
- `(deps)` - Dependencies
- `(docs)` - Documentation
- `(config)` - Configuration files
- `(ui)` - Frontend/templates

**Examples:**
- `feat: add user authentication system`
- `feat(excel): add AI validation endpoint`
- `fix(auth): correct email validation regex`
- `chore(deps): update Django to 5.1.2`
- `docs(readme): update installation instructions`
- `refactor(dashboard): extract chart component`

### File Naming
- Use UPPERCASE only for standard files: `README`, `LICENSE`, `CHANGELOG`
- Markdown files use dashes, not underscores: `static-files-workflow.md` ✅, `static_files_workflow.md` ❌
- Python files use underscores: `user_profile.py` ✅

### Code Style
- Follow PRM (Production Ready Mode) principles
- No comments in code unless specifically requested
- Use type hints for Python functions
- Templates: 2-space indentation
- Python: 4-space indentation (PEP 8)

### Django Specifics
- User model uses email (no username field)
- Always use `{% url %}` tags, never hardcode URLs
- Test with email-based authentication: `admin@example.com`
- Admin only available in DEBUG mode

### Template Organization (Enterprise Standard)
- **App templates:** `apps/<app_name>/templates/<app_name>/` (namespaced)
- **Global templates:** `/templates/` (base, partials, shared components)
- **Never mix:** Don't put app-specific templates in global `/templates/`
- **Example:** Dashboard templates go in `apps/dashboard/templates/dashboard/`

### Development Workflow
1. Always check existing patterns before creating new code
2. Run tests after changes with `pytest`
3. Verify Tailwind CSS builds when changing styles
4. Use `apps/core/` for Django utilities, `libs/` for pure Python
5. **NEVER auto-commit changes** - only commit when explicitly requested with "commit", "git commit", or similar explicit commands

### Testing Conventions
- Use pytest, not Django TestCase
- Tests go in `apps/*/tests/` folders (enterprise structure)
- Factories in `apps/*/tests/factories.py`
- Mark tests: `@pytest.mark.unit`, `@pytest.mark.integration`
- Coverage target: 70% minimum (current: 85.9%)

### Security
- Never commit secrets or `.env` files
- Always use environment variables for sensitive data
- Keep `DEBUG=False` in production settings

## Project Structure Overview
See [`docs/architecture.md`](./docs/architecture.md) for full details.

## Dependency Management
The project uses **pip-tools** for dependency locking (like Gemfile.lock/package-lock.json):

### Lock Files (✅ Committed to Git)
```
requirements/
├── base.txt          # High-level dependencies
├── base.lock         # Exact pinned versions (like Gemfile.lock)
├── development.txt   # Dev dependencies
├── development.lock  # Dev exact versions
├── production.txt    # Prod dependencies
├── production.lock   # Prod exact versions
└── test.lock         # Test exact versions
```

### Workflow
```bash
# Edit high-level requirements
vim requirements/development.txt

# Generate new lock file
pip-compile requirements/development.txt --output-file requirements/development.lock

# Install exact versions
pip-sync requirements/development.lock

# Update all dependencies
pip-compile --upgrade requirements/development.txt
```

## Code Quality Tools
The project uses modern Python tooling for code quality (like Prettier/RuboCop for other languages):

### Quick Quality Check
```bash
# Format code (auto-fix indentation, quotes, etc.)
black apps/

# Lint and fix issues
ruff check --fix apps/

# Type checking
mypy apps/

# Full quality workflow
ruff check --fix apps/ && black apps/ && mypy apps/
```

### Code Quality Configuration
- Pre-commit hooks configured in `.pre-commit-config.yaml`
- Black for formatting, Ruff for linting, MyPy for type checking
- Run `pre-commit run --all-files` to check all files

## Quick Commands
```bash
python manage.py runserver              # Start dev server
cd static_src && npm run dev            # Tailwind watch mode
pytest apps/<app_name>/                 # Run app tests
pytest -m unit                          # Run unit tests only
pytest --cov=apps                       # Run with coverage (86% current)

# Code quality
black apps/ && ruff check --fix apps/   # Format and lint

# Dependency management
pip-compile requirements/development.txt # Update lock file
pip-sync requirements/development.lock   # Install exact versions
```

## Key URLs
- `/auth/login/` - Email-based login (django-allauth)
- `/dashboard/` - Main application (requires login)
- `/admin/` - Django admin (DEBUG mode only)

---
*Last verified against codebase: 2025-09-20*
*Accuracy: 100%*