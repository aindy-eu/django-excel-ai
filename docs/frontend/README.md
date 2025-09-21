# Frontend Documentation

## Overview

Frontend architecture using Tailwind CSS for styling and hypermedia-driven JavaScript with HTMX + Alpine.js.

## 🆕 Recent Updates

- **NEW**: [`htmx-patterns.md`](./htmx-patterns.md) - Production HTMX patterns from US-008 implementation
- **UPDATED**: [`partials.md`](./partials.md) - Added HTMX partial guidelines and AI validation examples
- **ENHANCED**: HTMX state management patterns replacing Alpine.js complexity

## Documentation

### Core Architecture

- [`tailwind.md`](./tailwind.md) - Tailwind CSS setup, workflow, and build process
- [`javascript.md`](./javascript.md) - Modern JavaScript architecture with HTMX & Alpine.js
- [`partials.md`](./partials.md) - Template partials structure and organization (Updated with HTMX patterns)

### Production Patterns (NEW)

- [`htmx-patterns.md`](./htmx-patterns.md) - **Battle-tested HTMX patterns from real features**
  - Loading states with disabled buttons
  - Server-side state management
  - Partial template organization
  - Cost/metadata display patterns
  - Common anti-patterns to avoid

### Coming Soon

- `components.md` - Reusable UI components catalog
- `alpine-patterns.md` - Alpine.js component patterns

## Stack

- **CSS Framework**: Tailwind CSS 3.4 (JIT mode by default)
- **Build Tool**: PostCSS
- **JavaScript**: HTMX 1.9 + Alpine.js 3.x (hypermedia-driven)
- **Architecture**: Server-first, progressive enhancement
- **Icons**: Heroicons-style SVG icons

## Quick Start

```bash
# Install dependencies
cd static_src && npm install

# Development (watch mode)
npm run dev

# Production build
npm run build
```

## Principles

- **Server-first**: Django renders HTML, JavaScript enhances
- **Progressive Enhancement**: Works without JavaScript
- **Utility-first CSS**: Tailwind CSS with component extraction when repeated 3+ times
- **Hypermedia-driven**: HTMX for interactions, Alpine.js for reactive UI
- **Dark theme by default**: System preference aware
- **Mobile-first responsive design**: Tailwind breakpoints
- **State on server**: Avoid client/server state synchronization issues
- **Partial responses**: Return only what changes, not full pages

## Quick Reference

### When to Use What?

| Need            | Solution                 | Documentation                                                                           |
| --------------- | ------------------------ | --------------------------------------------------------------------------------------- |
| Form submission | HTMX                     | [`htmx-patterns.md`](./htmx-patterns.md#pattern-3-server-side-state-management)         |
| Loading states  | HTMX + Tailwind          | [`htmx-patterns.md`](./htmx-patterns.md#pattern-1-loading-states-with-disabled-buttons) |
| Dropdown/Modal  | Alpine.js                | [`javascript.md`](./javascript.md)                                                      |
| Data validation | HTMX partials            | [`partials.md`](./partials.md#htmx-response-patterns)                                   |
| Theme toggle    | Alpine.js + localStorage | [`javascript.md`](./javascript.md)                                                      |
| File upload     | HTMX + progress          | [`htmx-patterns.md`](./htmx-patterns.md)                                                |

### Key Files

```
docs/frontend/
├── README.md              # You are here
├── htmx-patterns.md       # Production HTMX patterns ⭐ NEW
├── javascript.md          # JS architecture overview
├── partials.md           # Template partials guide
└── tailwind.md           # Tailwind CSS setup
```
