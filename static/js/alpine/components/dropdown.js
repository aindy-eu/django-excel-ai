/**
 * Alpine.js Dropdown Component
 * Handles dropdown menus with keyboard navigation and click-outside-to-close
 */
document.addEventListener('alpine:init', () => {
    Alpine.data('dropdown', () => ({
        open: false,

        toggle() {
            this.open = !this.open;
        },

        close() {
            this.open = false;
        },

        // Keyboard navigation
        handleKeydown(event) {
            if (event.key === 'Escape') {
                this.close();
            }
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                this.toggle();
            }
        },

        // Click outside to close
        init() {
            this.$watch('open', (value) => {
                if (value) {
                    // Focus management for accessibility
                    this.$nextTick(() => {
                        const firstMenuItem = this.$el.querySelector('[role="menuitem"]');
                        if (firstMenuItem) {
                            firstMenuItem.focus();
                        }
                    });
                }
            });
        }
    }));
});