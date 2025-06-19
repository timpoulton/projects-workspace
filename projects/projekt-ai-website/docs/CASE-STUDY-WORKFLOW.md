# Case Study Workflow Documentation

This document outlines the standardized approach for creating and managing case studies on the Projekt AI website.

## Overview

The case study system uses a component-based approach with:

1. **JSON Data Model** - Structured content in a consistent format
2. **HTML Templates** - Dynamic templates using the Handlebars syntax
3. **Standardized CSS** - Using approved stylesheets only

## File Structure

```
/case-studies/
├── index.html                  # Case studies landing page
├── template-ultimate.html      # Master template with Handlebars syntax
├── case-study-schema.json      # JSON schema definition
├── data/                       # Individual case study data files
│   ├── reel-builder-automation.json
│   └── [other-case-study].json
└── [case-study-slug].html      # Generated case study pages
```

## Creating a New Case Study

### Step 1: Create the JSON data file

Create a new JSON file in the `case-studies/data/` directory following the schema structure:

```bash
# Example:
touch case-studies/data/new-case-study.json
```

Use `case-study-schema.json` as a reference for required fields and structure.

### Step 2: Fill in the case study content

Edit the JSON file with the case study content. Required sections:

- title and slug
- meta information
- hero section
- challenge and solution
- workflow steps
- results

### Step 3: Create the HTML file

Create a new HTML file for the case study using the correct stylesheet references:

```bash
node scripts/create-new-page.js case-studies/new-case-study.html --case-study
```

### Step 4: Integrate the template

Copy the content from `template-ultimate.html` into your new HTML file and adapt as needed for your specific case study.

## Templating System

The case study system uses a pseudo-Handlebars template syntax:

- `{{variable}}` - For simple variables
- `{{#each array}}...{{/each}}` - For iterating over arrays
- `{{#if condition}}...{{/if}}` - For conditional rendering

When generating production pages, these placeholders are replaced with actual content from the JSON data file.

## Case Study Schema

The schema ensures consistency across all case studies and includes the following main sections:

1. **Title and Meta** - Basic information and SEO details
2. **Hero Section** - Introduction and key statistics
3. **Challenge** - Problem statement and specific challenges
4. **Solution** - Overview and solution points
5. **Workflow** - Step-by-step breakdown of the implementation
6. **Results** - Impact metrics and testimonials
7. **Technical** - Implementation details and tech stack (optional)
8. **Related** - Links to related case studies
9. **CTA** - Call to action for visitors

## CSS Standards

Case study pages follow the Projekt AI CSS standards:

- Always include `main.css` and `case-study.css`
- Use the CSS variables defined in these stylesheets
- Follow the Extra Medium inspired design language

## Media Guidelines

- Hero videos should be high quality, under 2 minutes
- Images should be optimized for web (WebP format preferred)
- Include poster images for all videos
- Use a 16:9 aspect ratio for hero media

## Adding New Case Studies to Navigation

After creating a new case study, update the case studies index page with a link to your new case study:

```html
<a href="new-case-study.html" class="case-study-card">
  <img src="path/to/thumbnail.jpg" alt="Case Study Title">
  <h3>Case Study Title</h3>
  <p>Brief description</p>
</a>
```

## Best Practices

1. **Visual Documentation** - Include screenshots, diagrams, or videos
2. **Quantifiable Results** - Always include specific metrics
3. **Clean, Consistent Structure** - Follow the established pattern
4. **Technical Detail** - Include enough implementation details to provide value
5. **Narrative Flow** - Ensure the case study tells a coherent story 