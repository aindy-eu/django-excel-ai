# Tailwind CSS Setup

## Overview

Tailwind CSS v3.4 configuration and build process for the project.

## Directory Structure

```
static_src/          # Source files for Tailwind build
├── node_modules/    # Node dependencies (git-ignored)
├── package.json     # Node dependencies definition
├── tailwind.config.js
├── postcss.config.js
└── src/
    └── styles.css   # Main Tailwind input file

static/              # Development static files
├── css/
│   └── dist/
│       └── styles.css  # Compiled Tailwind output
└── js/              # JavaScript files

staticfiles/         # Production collected static files
                     # Created by: python manage.py collectstatic
                     # Git-ignored, server-generated
```

## Development Workflow

### 1. Initial Setup

```bash
cd static_src
npm install  # Install Tailwind v3.4 and dependencies
```

### Installed Plugins
- `@tailwindcss/forms` - Form element styling
- `@tailwindcss/typography` - Prose content styling
- `@tailwindcss/aspect-ratio` - Aspect ratio utilities
- `@tailwindcss/container-queries` - Container query support

### 2. Development Mode

```bash
# Terminal 1: Run Django server
python manage.py runserver

# Terminal 2: Run Tailwind in watch mode
cd static_src
npm run dev  # Watches for changes and rebuilds
```

### 3. Building for Production

```bash
cd static_src
npm run build  # Minified production CSS

# Then collect all static files
python manage.py collectstatic
```

## File Flow

1. **Edit Tailwind classes** → in templates or `static_src/src/styles.css`
2. **Tailwind builds** → outputs to `static/css/dist/styles.css`
3. **Django serves** → from `static/` in development
4. **Production collects** → all static files to `staticfiles/`

## Key Commands

```bash
# Development
npm run dev         # Watch mode with auto-rebuild

# Production
npm run build       # Minified production build
python manage.py collectstatic  # Collect for deployment

# Clean
rm -rf staticfiles/*  # Clear collected files
```

## Important Notes

- **Never edit** `static/css/dist/styles.css` directly (it's generated)
- **Git ignores** `node_modules/` and `staticfiles/`
- **Templates use** `{% load static %}` and `{% static 'css/dist/styles.css' %}`
- **Production serves** from `staticfiles/` (via whitenoise or nginx)

## Tailwind Configuration

Current setup uses Tailwind CSS v3 with:

- JIT (Just-In-Time) mode enabled
- Content paths configured for Django templates
- Custom color scheme (dark theme)
- Responsive breakpoints

See `static_src/tailwind.config.js` for full configuration.
