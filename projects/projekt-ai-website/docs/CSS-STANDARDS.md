# CSS Standards and Guidelines for Projekt AI Website

## Core Principles

1. **Consistency First**: Use approved stylesheets only
2. **Performance**: Minimize the number of CSS files loaded
3. **Maintainability**: Follow a modular approach
4. **Compatibility**: Ensure cross-browser and cross-device compatibility

## Approved Stylesheets

Only use the following stylesheets in HTML files:

1. **main.css** - Primary design system (required on all pages)
2. **case-study.css** - Additional styling for case studies only
3. **extramedium.css** - For pages using Extra Medium styling (optional)

## Deprecated Stylesheets

The following stylesheets should never be used in production:

- animations.css
- portfolio-dark-theme.css
- style.css
- dark-theme.css
- portfolio.css
- extramedium-inspired.css
- admin.css
- apple-dark-style.css

## Color Scheme

The color scheme is defined in CSS variables located in `main.css`:

```css
:root {
  --bg-primary: #000;
  --bg-secondary: #0a0a0a;
  --bg-tertiary: #1a1a1a;
  --bg-card: #1c1c1e;
  --bg-elevated: #2c2c2e;
  --text-primary: #fff;
  --text-secondary: #a1a1a6;
  --text-tertiary: #8e8e93;
  --accent-primary: #007aff;
  --accent-secondary: #00d4aa;
  --accent-gradient: linear-gradient(135deg, #007aff, #00d4aa);
}
```

## Typography

- Use the Inter font family for all text
- Include the following in the head section of all pages:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

## Page Templates

Use the following command to create a new page with the correct stylesheet references:

```bash
node scripts/create-new-page.js path/to/new-page.html [--case-study]
```

Example:
```bash
node scripts/create-new-page.js services/new-service.html
node scripts/create-new-page.js case-studies/new-case.html --case-study
```

## Standardizing Existing Pages

To fix CSS references in existing pages, run:

```bash
node scripts/fix-css-references.js
```

This will:
1. Scan all HTML files
2. Remove deprecated CSS references
3. Add standard CSS references if missing
4. Adjust relative paths based on file location

## The ExtraMedium-Inspired Design

The ExtraMedium design follows these principles:

1. Clean, minimalist aesthetic with ample white space
2. Large, clear typography with strong visual hierarchy
3. Reduced color palette focusing on text and subtle accents
4. Grid-based layouts with consistent spacing
5. Subtle animations and transitions for interactive elements

## Best Practices

1. Always use relative paths for CSS files (the scripts handle this automatically)
2. Test pages on multiple devices and browsers
3. Keep CSS selectors as simple as possible
4. Use CSS variables for colors, spacing, and typography
5. Avoid inline styles
6. Use BEM naming convention for custom components

## Text Gradient Effect

The blue gradient effect on headers is achieved using:

```css
h1 {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

To remove this effect, update the specific element to use regular text color:

```css
h1 {
  color: var(--text-primary);
  /* Remove gradient background, background-clip and -webkit-text-fill-color */
}
```

## Component Styling

Common components have standardized styling in the main.css file:

- Buttons (.btn, .btn-primary, .btn-secondary)
- Cards (.card, .card-elevated)
- Sections (.section, .hero, etc.)
- Navigation (header, nav, .nav-links)
- Form elements (inputs, textareas, etc.)

## Adding Custom CSS

If you need to add custom CSS for a specific page:

1. First, check if your styling needs can be met with existing CSS variables and classes
2. If custom CSS is necessary, add it to the appropriate stylesheet:
   - For global styles: main.css
   - For case study specific styles: case-study.css
   - For Extra Medium inspired pages: extramedium.css
3. Document new additions in this file 