# Template Partials

## Overview

Django template partials organized by domain for enterprise-scale maintainability.

## Structure

```
templates/partials/
├── auth/                 # Authentication components
├── forms/                # Form-related components
├── htmx/                 # HTMX response fragments (NEW)
├── navigation/           # Navigation components
└── ui/                   # Generic UI components
```

## Domains

### Navigation (`partials/navigation/`)

- `_main.html` - Main navigation wrapper
- `_mobile_menu.html` - Mobile menu button
- `_nav_authenticated.html` - Links for authenticated users
- `_nav_guest.html` - Links for guest users
- `_user_menu.html` - User dropdown menu

### Authentication (`partials/auth/`)

- `_buttons.html` - Sign in/Sign up buttons

### Forms (`partials/forms/`)

- `_field.html` - Reusable form field with label, input, and error handling

### UI Components (`partials/ui/`)

- `_theme_toggle.html` - Light/dark mode toggle with localStorage persistence

### HTMX Response Fragments (`partials/htmx/`)

- `_avatar_upload.html` - Avatar upload response with success message
- `_profile_cards.html` - Profile cards refresh after avatar change

## Usage

### Standard Includes

```django
{# In base template #}
{% include 'partials/navigation/_main.html' %}

{# In forms #}
{% include 'partials/forms/_field.html' with field=form.email %}

{# Conditional includes #}
{% if user.is_authenticated %}
  {% include 'partials/navigation/_nav_authenticated.html' %}
{% else %}
  {% include 'partials/navigation/_nav_guest.html' %}
{% endif %}
```

### HTMX Response Patterns

```python
# views.py
def validate_excel(request, pk):
    """Return different partials based on state."""
    try:
        validation = perform_validation()
        return render(request, 'excel_manager/partials/_ai_validation_result.html', {
            'validation': validation,
            'cached': False
        })
    except Exception as e:
        return render(request, 'excel_manager/partials/_ai_validation_error.html', {
            'error': str(e)
        })
```

### HTMX Target Updates

```html
<!-- Button triggers partial replacement -->
<button
  hx-post="{% url 'validate_ai' upload.pk %}"
  hx-target="#ai-validation-section"
  hx-swap="innerHTML"
>
  Validate
</button>

<!-- Target container -->
<div id="ai-validation-section">
  <!-- Partial will be inserted here -->
</div>
```

## Dark Mode Support

All partials support automatic light/dark mode switching using Tailwind CSS classes:

- `dark:` prefix for dark mode variants
- `transition-colors duration-200` for smooth transitions
- Theme preference stored in localStorage

## Best Practices

### General Principles

1. **Domain Separation**: Group partials by functionality, not location
2. **Naming Convention**: Use underscore prefix (`_partial.html`)
3. **Self-Contained**: Partials should work independently
4. **Documentation**: Comment complex partials
5. **DRY Principle**: Extract when used 3+ times

### HTMX-Specific Guidelines

1. **State Partials**: Create separate partials for each state (loading, success, error)
2. **Target IDs**: Ensure container IDs match `hx-target` attributes exactly
3. **Response Size**: Keep HTMX partials minimal - only what changes
4. **Context Passing**: Pass all required context from views to partials
5. **No JavaScript**: HTMX partials should not contain inline JavaScript

### Advanced HTMX Patterns (In Production)
- **Force refresh**: `hx-vals='{"force_refresh": "true"}'` bypasses caching
- **Swap strategies**: `hx-swap="outerHTML"` replaces entire elements
- **Event debugging**: `hx-on:htmx:afterRequest` for monitoring
- **Note**: `hx-swap-oob` mentioned in theory but not implemented

### Partial Organization Pattern

```
app_name/templates/app_name/partials/
├── _feature.html                 # Full feature display
├── _feature_loading.html         # Loading state
├── _feature_result.html          # Success state
├── _feature_error.html           # Error state
└── _feature_empty.html           # Empty state
```

## App-Specific Partials

Apps maintain their own partials within their template directories:

```
apps/users/templates/users/partials/
├── _profile_info_card.html
├── _profile_detail_item.html
└── _settings_card.html

apps/excel_manager/templates/excel_manager/partials/
├── _data_table.html              # Excel data display table
├── _file_list.html               # List of uploaded Excel files
├── _upload_area.html             # Drag-and-drop upload zone
├── _ai_validation_result.html   # AI validation results (HTMX)
├── _ai_validation_error.html    # AI validation error state (HTMX)
└── _ai_validation_loading.html  # AI validation loading state (HTMX)
```

This keeps app-specific components isolated while global partials remain in `templates/partials/`.
