# Projekt-AI Website – Style Guide

This document summarises the **design-system CSS** used across the site so everyone can reference a single source of truth.

## Core Stylesheets

| File | Purpose |
|------|---------|
| `assets/css/main.css` | Global dark-theme design-system (colour tokens, typography scale, layout utilities, buttons, navigation, etc.) |
| `assets/css/case-study.css` | Add-on rules for long-form case-study / proposal pages (hero grids, challenge/solution columns, process steps, metrics cards). |

**Deprecated / NOT to be used**
• `portfolio-dark.css` (legacy) – replaced by `main.css`.
• Any inline "Extra-Medium replica" styles inside old proto pages.

## Colour Tokens (defined in `:root` in `main.css`)

```
--bg-primary:   #0a0a0a;
--bg-secondary: #1a1a1a;
--accent-primary:  #00d4ff;
--accent-secondary: #ff006e;
--text-primary: #ffffff;
--text-secondary: #e5e5e5;
```

## Type Scale
```
--font-size-base: 1rem;  /*16px*/
--font-size-4xl: 2.25rem;/*36px*/
--font-size-5xl: 3rem;   /*48px*/
```

## Layout Utilities (examples)
```
.container       { max-width: 1400px; margin:0 auto; padding:0 var(--space-lg); }
.grid-2          { display:grid; grid-template-columns:1fr 1fr; gap:var(--space-xl); }
.flex-center     { display:flex; align-items:center; justify-content:center; }
.btn-primary     { @apply .btn .btn-primary; }  /* pre-built in main.css */
```

## Section Patterns
1. **Hero (case study)** – `.case-study-header > .case-study-content` uses two-column grid.
2. **Challenge / Solution** – `.problem-solution-grid` two columns with icon column.
3. **Workflow Steps** – `.workflow-steps` flex row with `.workflow-step` cards and connecting `→` arrows.
4. **Stats Preview** – `.results-preview .result-stat` for headline metrics.

## How to add pages
1. Link the stylesheets:
```html
<link rel="stylesheet" href="/assets/css/main.css">
<link rel="stylesheet" href="/assets/css/case-study.css"><!-- if needed -->
```
2. Use existing classes; avoid adding inline styles or new colours unless they are added to `main.css` first.

---
_Last updated: 2025-06-18_ 