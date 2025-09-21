# HTMX Production Patterns

> Battle-tested patterns from real feature implementation

## Overview

These patterns emerged from implementing US-008 (AI Excel Validation) and represent production-ready solutions to common HTMX challenges. Unlike theoretical examples, each pattern here has been tested under real conditions.

## Pattern 1: Loading States with Disabled Buttons

### The Problem

Users click buttons multiple times during async operations, causing duplicate requests.

### The Solution

Combine HTMX's `hx-disabled-elt` with Tailwind's disabled utilities:

```html
<button
  hx-post="/validate/"
  hx-target="#results"
  hx-disabled-elt="this"
  class="bg-blue-600 hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:bg-blue-600"
>
  Validate
</button>
```

**Why this works:**

- `hx-disabled-elt="this"` - HTMX adds `disabled` attribute during request
- Tailwind's `disabled:` utilities provide visual feedback
- No JavaScript required

## Pattern 2: Inline Loading Indicators

### The Problem

Need to show loading state without replacing entire content area.

### The Solution

Use HTMX indicators with CSS classes:

```html
<button hx-post="/action/" hx-indicator="#my-button" id="my-button">
  <!-- Hidden spinner, shown during request -->
  <svg class="htmx-indicator animate-spin h-5 w-5 mr-2">
    <!-- spinner SVG -->
  </svg>
  <!-- Normal icon, hidden during request -->
  <svg class="w-5 h-5 mr-2">
    <!-- normal icon -->
  </svg>
  <!-- Text that swaps -->
  <span class="htmx-indicator">Loading...</span>
  <span>Click Me</span>
</button>

<style>
  /* Hide indicators by default */
  .htmx-indicator {
    display: none !important;
  }
  /* Show during request - can also use flex */
  .htmx-request .htmx-indicator {
    display: inline-block !important; /* or flex !important */
  }
  /* Hide non-indicators during request */
  .htmx-request button > span:not(.htmx-indicator) {
    display: none !important;
  }
</style>
```

## Pattern 3: Server-Side State Management

### The Problem

Alpine.js and HTMX state can get out of sync, causing UI bugs.

### The Solution

Let the server manage all state:

```python
# views.py
class ValidateView(View):
    def post(self, request, pk):
        # Check cache on server
        if has_cached_result():
            return render(request, 'partials/cached_result.html', {
                'cached': True
            })

        # Perform validation
        result = validate()
        return render(request, 'partials/fresh_result.html', {
            'result': result
        })
```

```html
<!-- Let HTMX replace entire section -->
<div id="validation-section">
  <!-- Server decides what to show -->
  {% if not validated %}
  <button hx-post="/validate/" hx-target="#validation-section">Validate</button>
  {% else %} {% include "partials/validation_result.html" %} {% endif %}
</div>
```

**Avoid this Alpine.js complexity:**

```html
<!-- DON'T: Complex client state -->
<div x-data="{ validating: false, cached: false }">
  <!-- State sync nightmares -->
</div>
```

## Pattern 4: Partial Template Organization

### The Problem

HTMX responses need different templates than full page renders.

### The Solution

Consistent partial organization:

```
templates/
└── app_name/
    ├── page.html                    # Full page
    └── partials/
        ├── _result.html             # Success response
        ├── _error.html              # Error response
        └── _loading.html            # Loading state
```

View pattern:

```python
def my_view(request):
    try:
        result = perform_action()
        template = 'partials/_result.html'
        context = {'result': result}
    except Exception as e:
        template = 'partials/_error.html'
        context = {'error': str(e)}

    return render(request, f'app_name/{template}', context)
```

## Pattern 5: Force Refresh with Cache Bypass

### The Problem

Cached results are stale but user needs fresh data.

### The Solution

Explicit user control over caching:

```html
<button
  hx-post="/validate/"
  hx-vals='{"force_refresh": "true"}'
  hx-target="#results"
  class="text-sm text-blue-600"
>
  Force Refresh
</button>
```

```python
def validate_view(request):
    force_refresh = request.POST.get('force_refresh') == 'true'

    if not force_refresh and has_cache():
        return cached_result()

    return fresh_validation()
```

## Pattern 6: Cost/Metadata Display

### The Problem

Need to show dynamic metadata (cost, tokens, timing) after async operations.

### The Solution

Include metadata in response template:

```html
<!-- partials/_validation_result.html -->
<div class="results">
  <!-- Main content -->
  {{ validation.content }}

  <!-- Metadata footer -->
  <div class="text-xs text-gray-500 mt-4">
    <span>Cost: ${{ validation.cost|floatformat:4 }}</span>
    <span>Tokens: {{ validation.total_tokens }}</span>
    <span>Model: {{ validation.ai_metadata.model|default:"Claude 4 Sonnet" }}</span>
    <span>Time: {{ validation.ai_metadata.response_time_ms|floatformat:0 }}ms</span>
  </div>
</div>
```

## Pattern 7: Graceful Degradation

### The Problem

Service might be unavailable or disabled.

### The Solution

Check availability server-side:

```python
def validate_view(request):
    if not settings.AI_FEATURES_ENABLED:
        return render(request, 'partials/_feature_disabled.html', {
            'message': 'AI features are currently disabled'
        })

    try:
        result = ai_service.validate()
    except ServiceUnavailable:
        return render(request, 'partials/_service_error.html', {
            'message': 'Service temporarily unavailable'
        })
```

## Pattern 8: HTMX-Compatible CSRF

### The Problem

Django's CSRF protection needs to work with HTMX.

### The Solution

Auto-inject CSRF token:

```javascript
// static/js/utils/csrf.js
document.body.addEventListener("htmx:configRequest", (event) => {
  event.detail.headers["X-CSRFToken"] = document.querySelector("[name=csrfmiddlewaretoken]").value;
});
```

Load after HTMX:

```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
<script src="{% static 'js/utils/csrf.js' %}"></script>
```

## Pattern 9: Delete with Confirmation

### The Problem

Destructive actions need confirmation.

### The Solution

Use HTMX's built-in confirm:

```html
<button
  hx-post="{% url 'delete' item.pk %}"
  hx-confirm="Are you sure you want to delete {{ item.name }}?"
  hx-target="#item-list"
  class="text-red-600"
>
  Delete
</button>
```

## Pattern 10: Target ID Consistency

### The Problem

HTMX can't find target, throws `htmx:targetError`.

### The Solution

Ensure target IDs match between trigger and container:

```html
<!-- Container -->
<div id="excel-file-list">
  <!-- Content -->
</div>

<!-- Trigger - must match exactly -->
<button hx-target="#excel-file-list">
  <!-- ✅ Correct -->
  <button hx-target="#file-list"><!-- ❌ Wrong --></button>
</button>
```

## Anti-Patterns to Avoid

### 1. Mixing Alpine.js State with HTMX Updates

```html
<!-- AVOID: State sync issues -->
<div x-data="{ items: [] }">
  <button hx-get="/items/" hx-target="#list">
    <!-- Alpine won't know items changed -->
  </button>
</div>
```

### 2. Client-Side DOM Manipulation with HTMX

```html
<!-- AVOID: Interferes with HTMX -->
<button
  @click="document.getElementById('content').innerHTML = 'Loading...'"
  hx-post="/action/"
></button>
```

### 3. Multiple State Sources

```html
<!-- AVOID: Which is truth? -->
<div x-data="{ validating: false }" hx-get="/status/">
  <!-- Server says one thing, Alpine says another -->
</div>
```

## Testing Patterns

### 1. Test HTMX Responses

```python
def test_htmx_validation(client):
    response = client.post(
        '/validate/',
        HTTP_HX_REQUEST='true'  # Simulate HTMX
    )
    assert 'partial' in response.template_name
```

### 2. Test Loading States

```javascript
// Check indicator appears
document.querySelector("button").click();
assert(document.querySelector(".htmx-indicator").style.display !== "none");
```

## Performance Optimizations

### 1. Swap Strategies

```html
<!-- Fastest: outerHTML -->
<div hx-swap="outerHTML">
  <!-- Smooth: with transition -->
  <div hx-swap="outerHTML transition:true">
    <!-- Preserve: innerHTML for containers -->
    <div hx-swap="innerHTML"></div>
  </div>
</div>
```

### 2. Debounced Triggers

```html
<!-- Prevent rapid-fire requests -->
<input hx-post="/search/" hx-trigger="keyup changed delay:500ms" hx-target="#results" />
```

### 3. Lazy Loading

```html
<!-- Load when visible -->
<div hx-get="/content/" hx-trigger="revealed">
  <div class="skeleton-loader">Loading...</div>
</div>
```

## Decision Matrix

| Scenario                    | Use HTMX | Use Alpine.js | Use Both |
| --------------------------- | -------- | ------------- | -------- |
| Form submission             | ✅       |               |          |
| Loading indicators          | ✅       |               |          |
| Modal open/close            |          | ✅            |          |
| Tab switching (no server)   |          | ✅            |          |
| Tab switching (server data) |          |               | ✅       |
| Real-time validation        | ✅       |               |          |
| Client-only filtering       |          | ✅            |          |
| Infinite scroll             | ✅       |               |          |
| Tooltips                    |          | ✅            |          |

## Key Learnings

1. **Server state is truth** - Don't duplicate state client-side
2. **HTMX indicators are powerful** - Use CSS classes, not JavaScript
3. **Partials are your friend** - Small, focused templates
4. **Let HTMX handle disabled state** - `hx-disabled-elt` + Tailwind
5. **User control matters** - Force refresh, confirmations
6. **Test the request type** - `request.htmx` in Django views

## Conclusion

These patterns represent real production solutions, not theoretical best practices. Each emerged from actual problems encountered during feature development. By following these patterns, you can avoid the state synchronization issues we discovered and build robust HTMX applications that are maintainable and performant.

---
*Last verified against codebase: 2025-01-19*
