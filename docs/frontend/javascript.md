# JavaScript Architecture

## Overview

Modern JavaScript architecture for Django using Hypermedia-Driven patterns with HTMX and Alpine.js.

## Philosophy

- **Server-First**: Django renders HTML, not JSON APIs
- **Progressive Enhancement**: Works without JavaScript
- **Minimal Complexity**: No build steps, no state management
- **Team Efficiency**: One team, one codebase

## Tech Stack

### HTMX (Hypermedia Exchange)

```html
<!-- AJAX without JavaScript -->
<button hx-get="/api/users" hx-target="#user-list" hx-swap="innerHTML">Load Users</button>
```

**Use Cases:**

- Dynamic content loading
- Form submissions without page reload
- Infinite scroll
- Real-time updates via SSE

### Alpine.js (Reactive Components)

```html
<!-- Declarative reactive UI -->
<div x-data="{ open: false, count: 0 }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open" x-transition>
    <button @click="count++">Count: <span x-text="count"></span></button>
  </div>
</div>
```

**Use Cases:**

- Dropdowns, modals, tabs
- Client-side validation
- Interactive UI components
- Local state management

## Project Structure

```
static/
├── js/
│   ├── alpine/
│   │   └── components/           # Individual Alpine.js components
│   │       ├── avatarUpload.js  # Avatar upload with drag-drop
│   │       ├── dropdown.js       # Navigation dropdown
│   │       ├── excelUpload.js   # Excel file upload
│   │       └── theme.js          # Dark/light theme toggle
│   └── utils/
│       └── csrf.js               # Django CSRF handling for HTMX

templates/
├── components/              # Server components
│   ├── _modal.html
│   ├── _dropdown.html
│   └── _tabs.html
├── partials/
│   └── htmx/               # HTMX response fragments
│       ├── _user_row.html
│       ├── _form_errors.html
│       └── _notification.html
```

## Integration Patterns

### 1. HTMX + Django Views

```python
# views.py
def user_list(request):
    if request.htmx:
        # Return partial for HTMX request
        return render(request, 'partials/htmx/_user_list.html', context)
    # Return full page for normal request
    return render(request, 'users/list.html', context)
```

### 2. Alpine.js Components

```javascript
// alpine/components/modal.js
Alpine.data("modal", () => ({
  open: false,
  title: "",

  show(title) {
    this.title = title;
    this.open = true;
  },

  hide() {
    this.open = false;
  },
}));
```

### 3. Django + Alpine Data

```django
<!-- Pass Django context to Alpine -->
<div x-data='{
    user: {{ user_data|json_script:"user-data" }},
    settings: {{ settings|json_script:"settings-data" }}
}'>
    <!-- Alpine component using Django data -->
</div>
```

## Best Practices

### 1. Progressive Enhancement

```html
<!-- Works without JS -->
<form method="POST" action="{% url 'submit' %}" hx-post="{% url 'submit' %}" hx-target="#result">
  <!-- Form fields -->
</form>
```

### 2. CSRF Protection

```javascript
// utils/csrf.js - Enterprise pattern: separate concerns
document.addEventListener("DOMContentLoaded", function () {
  document.body.addEventListener("htmx:configRequest", (event) => {
    const csrfToken =
      document.querySelector("[name=csrfmiddlewaretoken]")?.value ||
      document.querySelector("meta[name=csrf-token]")?.content;
    if (csrfToken) {
      event.detail.headers["X-CSRFToken"] = csrfToken;
    }
  });
});
```

### 3. Component Registration (Individual Files Pattern)

```javascript
// alpine/components/theme.js - Individual component approach
document.addEventListener('alpine:init', () => {
    Alpine.data('themeToggle', () => ({
        isDark: localStorage.getItem('theme') === 'dark' ||
                (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches),

        init() {
            this.applyTheme(this.isDark ? 'dark' : 'light');
        },

        toggle() {
            this.isDark = !this.isDark;
            this.applyTheme(this.isDark ? 'dark' : 'light');
        },

        applyTheme(theme) {
            localStorage.setItem('theme', theme);
            document.documentElement.classList.toggle('dark', theme === 'dark');
        }
    }));
});
```

**Current Implementation Pattern:**

- ✅ Each component in its own file
- ✅ Clear, focused components
- ✅ Easy to understand and maintain
- ✅ Loaded individually in base template
- ✅ Standard Alpine.js approach

### 3. Component Organization

```html
<!-- Reusable component pattern -->
<div
  x-data="dropdown"
  x-init="$watch('open', value => $dispatch('dropdown-changed', value))"
  class="relative"
>
  <!-- Component HTML -->
</div>
```

### 4. Error Handling

```html
<!-- HTMX error handling -->
<div hx-get="/api/data" hx-trigger="click" hx-on:htmx:response-error="handleError($event)">
  Load Data
</div>
```

## Common Patterns

### Infinite Scroll

```html
<div hx-get="/posts?page=2" hx-trigger="revealed" hx-swap="afterend">Loading more...</div>
```

### Live Search

```html
<input
  type="search"
  name="q"
  hx-get="/search"
  hx-trigger="keyup changed delay:500ms"
  hx-target="#search-results"
/>
```

### Modal with Alpine

```html
<div x-data="{ open: false }" @keydown.escape.window="open = false">
  <button @click="open = true">Open Modal</button>

  <div x-show="open" x-transition class="fixed inset-0 bg-black bg-opacity-50">
    <!-- Modal content -->
  </div>
</div>
```

## Performance Considerations

1. **Lazy Loading**: Use HTMX's `hx-trigger="revealed"` for lazy loading
2. **Debouncing**: Use `delay:500ms` for search inputs
3. **Caching**: Leverage `hx-boost` for navigation caching
4. **Bundle Size**: HTMX (~14kb) + Alpine.js (~13.5kb) = ~27.5kb total

## Testing

### HTMX Responses

```python
# tests.py
def test_htmx_request(self):
    response = self.client.get(
        '/users/',
        HTTP_HX_REQUEST='true'
    )
    self.assertTemplateUsed(response, 'partials/htmx/_user_list.html')
```

### Alpine Components

```javascript
// Use Alpine's test utilities
test("dropdown toggles", async () => {
  const component = Alpine.data("dropdown")();
  component.toggle();
  expect(component.open).toBe(true);
});
```

## Migration Path

### From jQuery

```javascript
// jQuery
$("#button").click(function () {
  $.get("/api/data", function (data) {
    $("#result").html(data);
  });
});

// HTMX
<button hx-get="/api/data" hx-target="#result">
  Click
</button>;
```

### From React/Vue

```javascript
// React Component
function UserList() {
    const [users, setUsers] = useState([]);
    useEffect(() => { /* fetch users */ }, []);
    return <div>{users.map(...)}</div>;
}

// HTMX + Alpine
<div hx-get="/users" hx-trigger="load">
    <!-- Server renders the list -->
</div>
```

## Current Implementation

### Components in Production

1. **Theme Toggle** (`themeToggle`) - Dark/light mode switching with localStorage persistence
2. **Mobile Navigation** (`dropdown`) - Responsive mobile menu with accessibility features
3. **CSRF Protection** (`utils/csrf.js`) - Automatic CSRF token injection for HTMX requests

### Template Usage Examples

```html
<!-- Theme toggle component -->
<div x-data="themeToggle">
  <button @click="toggle" :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'">
    <svg x-show="isDark" x-transition><!-- Sun icon --></svg>
    <svg x-show="!isDark" x-transition><!-- Moon icon --></svg>
  </button>
</div>

<!-- Mobile navigation dropdown -->
<nav x-data="dropdown" @keydown.escape.window="close">
  <button @click="toggle" :aria-expanded="open">Menu</button>
  <div x-show="open" x-transition @click.away="close">
    <!-- Menu items -->
  </div>
</nav>

<!-- HTMX with Django CSRF (automatic) -->
<button hx-get="/profile/emails" hx-target="#email-card">Manage Emails</button>
```

## Resources

- [HTMX Documentation](https://htmx.org)
- [Alpine.js Documentation](https://alpinejs.dev)
- [django-htmx Package](https://github.com/adamchainz/django-htmx)
- [Hypermedia Systems Book](https://hypermedia.systems)

## Decision Matrix

| Use Case          | Solution                      |
| ----------------- | ----------------------------- |
| Page navigation   | HTMX with `hx-boost`          |
| Form submission   | HTMX with validation partials |
| Dropdowns/Modals  | Alpine.js                     |
| Real-time updates | HTMX with SSE                 |
| Complex state     | Alpine.js stores              |
| Animations        | Alpine.js transitions         |
| API integration   | HTMX or fetch() in Alpine     |

---
*Last verified against codebase: 2025-01-19*
