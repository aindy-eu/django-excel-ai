# Development Guide

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (running and accessible)
- Node.js 18+ (for Tailwind CSS)
- System dependency: `libmagic1` (for file type detection)

### Initial Setup

1. **Clone and environment setup**
```bash
git clone <repository>
cd django-excel-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install libmagic1 postgresql-client

# Install Python and Node.js dependencies
pip install -r requirements/development.txt
cd static_src && npm install && cd ..
```

3. **Database setup**
```bash
createdb dashboard_db
cp .env.example .env  # Edit with your database credentials
python manage.py migrate
python manage.py createsuperuser  # Uses email, not username
```

4. **Run development servers**
```bash
# Option 1: Use the convenience script (for Docker/DevContainer or if PostgreSQL is running)
./dev-start.sh  # Waits for DB, runs migrations, creates admin@example.com, starts both servers

# Option 2: Manual start (recommended for local development)
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Tailwind CSS (watch mode)
cd static_src && npm run dev
```

## Development Commands

### Database
```bash
python manage.py makemigrations       # Create new migrations
python manage.py migrate              # Apply migrations
python manage.py showmigrations       # View migration status
python manage.py dbshell             # PostgreSQL shell
```

### User Management
```bash
python manage.py createsuperuser      # Create admin (email-based)
python manage.py changepassword <email>  # Change user password
```

### Static Files
```bash
cd static_src
npm run dev                           # Development watch mode
npm run build                         # Production build
python manage.py collectstatic        # Collect for deployment
```

### Testing (Pytest)
```bash
pytest                                # Run all tests
pytest apps/users/                    # Test specific app
pytest -m unit                       # Run unit tests only
pytest -m integration                # Run integration tests
pytest --cov=apps                     # Run with coverage report
pytest -n auto                       # Run tests in parallel
```

#### Test Organization
- Tests are in `apps/*/tests/` folders (enterprise structure)
- Test factories in `apps/*/tests/factories.py`
- Coverage target: 70% minimum
- Markers: unit, integration, slow, auth, model, view, api

### Shell Access
```bash
python manage.py shell                # Django shell
python manage.py shell_plus           # Enhanced shell (if installed)
```

## Development URLs

- `http://localhost:8000/` - Homepage
- `http://localhost:8000/auth/login/` - Login (email-based)
- `http://localhost:8000/auth/signup/` - Registration (email-based)
- `http://localhost:8000/dashboard/` - Dashboard (login required)
- `http://localhost:8000/admin/` - Django admin

## Environment Variables

Required in `.env`:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=dashboard_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Optional: AI Features
ANTHROPIC_API_KEY=sk-ant-your-key-here
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=1024
AI_FEATURES_ENABLED=True
```

## Code Quality Tools

### Formatting & Linting
```bash
# Format Python code
black apps/

# Lint Python code
ruff check --fix apps/

# Type checking
mypy apps/

# All quality checks
black apps/ && ruff check --fix apps/ && mypy apps/
```

### Pre-commit Hooks
```bash
# Install git hooks (one-time setup)
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### Dependency Management
```bash
# Using pip-tools for locked dependencies
pip-compile requirements/development.txt  # Update lock file
pip-sync requirements/development.lock    # Install exact versions
```

## Code Style

- Python: PEP 8 (enforced by Black)
- Templates: 2-space indentation
- JavaScript: ES6+
- CSS: Tailwind utility classes

## Common Issues

### Tailwind not updating
```bash
cd static_src
npm run build
# Restart Django server
```

### Migration conflicts
```bash
python manage.py migrate --fake-zero <app_name>
python manage.py migrate <app_name>
```

### Static files not loading
```bash
python manage.py collectstatic --clear
```