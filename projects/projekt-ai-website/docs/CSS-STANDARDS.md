# CSS Standards for Projekt-AI Website

## Core Stylesheets

The Projekt-AI website uses a streamlined CSS approach with **only two approved stylesheets**:

1. **`/assets/css/main.css`** - Global design system
   - Core layout and typography
   - Color schemes and variables
   - Responsive grid system
   - Component styling (buttons, cards, etc.)

2. **`/assets/css/case-study.css`** - Add-on rules specific to case study pages
   - Special layouts for case studies
   - Project showcase components
   - Process visualization styles
   - Results presentation

## Implementation Rules

### For All Pages:

```html
<link rel="stylesheet" href="/assets/css/main.css">
```

### For Case Study Pages Only:
```html
<link rel="stylesheet" href="/assets/css/main.css">
<link rel="stylesheet" href="/assets/css/case-study.css">
```

## ⚠️ Legacy Files - DO NOT USE

The following CSS files are deprecated and should **never** be included:

- `portfolio-dark.css`
- `portfolio-dark-theme.css` 
- `style.css`
- `dark-theme.css`
- `extramedium-inspired.css`
- `animations.css`
- `portfolio.css`
- `apple-dark-style.css`

## Tools to Maintain CSS Standards

### Fix CSS References

To automatically fix incorrect CSS references across the site:

```bash
cd projects/projekt-ai-website
node scripts/fix-css-references.js
```

This script:
- Removes references to deprecated CSS files
- Ensures all pages include `main.css`
- Adds `case-study.css` to case study pages if missing

### Create New Pages

To create new pages with the correct CSS references:

```bash
cd projects/projekt-ai-website
node scripts/create-new-page.js ./path/to/new-page.html "Page Title" "Description" [is-case-study]
```

Example for standard page:
```bash
node scripts/create-new-page.js ./services/new-service.html "New Service" "Service description" false
```

Example for case study:
```bash
node scripts/create-new-page.js ./case-studies/new-case.html "New Case Study" "Case study description" true
```

## Best Practices

1. **Never manually edit the HTML head** to add your own CSS files
2. **Use CSS variables** from `main.css` for consistency
3. **Add custom styles inline** using `<style>` tags if needed for one-off pages
4. **Run the fix-css-references.js script** before any deployment
5. **Use the create-new-page.js script** to generate new pages

## Testing

Before deploying new pages:

1. Validate CSS references
2. Check mobile responsiveness
3. Verify dark mode compatibility
4. Test page load performance 