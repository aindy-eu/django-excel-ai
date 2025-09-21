/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  content: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
    '../../dashboard/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}