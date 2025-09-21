/**
 * Django CSRF Token Handling for HTMX
 * Configures HTMX to automatically include Django CSRF tokens
 */
document.addEventListener('DOMContentLoaded', function() {
    // Configure HTMX to include CSRF token in all requests
    document.body.addEventListener('htmx:configRequest', (event) => {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
            || document.querySelector('meta[name=csrf-token]')?.content
            || window.CSRF_TOKEN;

        if (csrfToken) {
            event.detail.headers['X-CSRFToken'] = csrfToken;
        }
    });
});