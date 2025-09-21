/**
 * Alpine.js Theme Toggle Component
 * Handles dark/light mode switching with localStorage persistence
 */
document.addEventListener('alpine:init', () => {
    Alpine.data('themeToggle', () => ({
        isDark: false,

        init() {
            // Initialize theme on component load
            this.isDark = this.getCurrentTheme() === 'dark';
            this.applyTheme(this.isDark ? 'dark' : 'light');

            // Listen for system theme changes
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                // Only apply if user hasn't manually set a preference
                if (!localStorage.getItem('theme')) {
                    this.isDark = e.matches;
                    this.applyTheme(this.isDark ? 'dark' : 'light');
                }
            });
        },

        getCurrentTheme() {
            const storedTheme = localStorage.getItem('theme');
            if (storedTheme) {
                return storedTheme;
            }
            // Check system preference
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        },

        applyTheme(theme) {
            if (theme === 'dark') {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
            localStorage.setItem('theme', theme);
        },

        toggle() {
            this.isDark = !this.isDark;
            this.applyTheme(this.isDark ? 'dark' : 'light');

            // Dispatch event for other components that might need to know
            this.$dispatch('theme-changed', { isDark: this.isDark });
        }
    }));
});