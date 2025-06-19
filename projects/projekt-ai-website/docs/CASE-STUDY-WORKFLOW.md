# Case Study Creation Workflow

This document outlines the process for creating new case studies for the Projekt AI website, following the Extra Medium-inspired design system.

## Overview

The case study creation process follows these steps:

1. Create JSON data file with case study content
2. Generate HTML from the template using the JSON data
3. Review and make any custom adjustments (if needed)
4. Deploy to production

## Directory Structure

- `/case-studies/` - Published case study HTML files
- `/case-studies/data/` - JSON data files for case studies
- `/case-studies/template-extramedium.html` - Main template file
- `/scripts/generate-case-study.js` - Generator script

## Creating a New Case Study

### Step 1: Create JSON Data File

Create a new JSON file in `/case-studies/data/` using the following format:

```json
{
  "id": "unique-case-study-id",
  "title": "Case Study Title",
  "subtitle": "Brief description of the project",
  "category": "Category (e.g., Social Media Automation)",
  "industry": "Industry (e.g., Music Production)",
  "description": "Meta description for SEO",
  "client_name": "Client Name",
  "services": "Services Provided (comma separated)",
  "year": "Year Completed",
  "featured_image": "../assets/img/portfolio/image-name.jpg",
  "overview_text": "Detailed overview paragraph",
  "challenge": {
    "text": "Description of the challenge",
    "points": [
      "Challenge point 1",
      "Challenge point 2",
      "Challenge point 3"
    ]
  },
  "solution": {
    "text": "Description of the solution",
    "points": [
      "Solution point 1",
      "Solution point 2",
      "Solution point 3"
    ]
  },
  "process": {
    "intro": "Introduction to the process",
    "steps": [
      {
        "title": "Step 1 Title",
        "text": "Step 1 description"
      },
      {
        "title": "Step 2 Title",
        "text": "Step 2 description"
      },
      {
        "title": "Step 3 Title",
        "text": "Step 3 description"
      },
      {
        "title": "Step 4 Title",
        "text": "Step 4 description"
      }
    ]
  },
  "video_info": {
    "intro": "Description of the video",
    "source": "../assets/videos/video-name.mp4",
    "poster": "../assets/img/portfolio/video-poster.jpg",
    "caption": "Video caption text"
  },
  "results": {
    "text": "Description of the results",
    "metrics": [
      {
        "value": "95%",
        "label": "Metric 1 label"
      },
      {
        "value": "$1000",
        "label": "Metric 2 label"
      },
      {
        "value": "24hrs",
        "label": "Metric 3 label"
      }
    ]
  },
  "related_projects": [
    {
      "id": "related-project-1",
      "title": "Related Project 1",
      "image": "../assets/img/portfolio/related-1-card.jpg",
      "url": "related-project-1.html"
    },
    {
      "id": "related-project-2",
      "title": "Related Project 2",
      "image": "../assets/img/portfolio/related-2-card.jpg",
      "url": "related-project-2.html"
    },
    {
      "id": "related-project-3",
      "title": "Related Project 3",
      "image": "../assets/img/portfolio/related-3-card.jpg",
      "url": "related-project-3.html"
    }
  ]
}
```

### Step 2: Generate HTML

From the project root directory, run:

```bash
node scripts/generate-case-study.js your-case-study-id
```

Or to generate all case studies:

```bash
node scripts/generate-case-study.js
```

This will create an HTML file in the `/case-studies/` directory based on your JSON data.

### Step 3: Review & Customize

Open the generated HTML file and review it for any issues. Make any custom adjustments if needed. The generated file follows the Extra Medium design system with:

- Clean, minimalist design
- Proper typography and spacing
- Mobile-responsive layout
- Consistent branding elements

### Step 4: Add Images & Videos

Make sure all referenced images and videos exist in the proper directories:

- Case study featured images: `/assets/img/portfolio/`
- Video content: `/assets/videos/`

### Step 5: Update Homepage

Add the new case study to the projects grid on the homepage `index-extramedium.html`.

### Step 6: Deploy

Commit your changes and push to deploy the updated site to Netlify.

## Design Guidelines

When creating case study content, follow these guidelines:

1. **Headlines** - Keep titles under 60 characters
2. **Paragraphs** - Keep paragraphs short and focused (2-4 sentences)
3. **Metrics** - Use concrete, impressive numbers when possible
4. **Images** - Use high-quality images with proper dimensions
5. **Videos** - Keep videos short (1-2 minutes) and focused on results

## Custom HTML Elements

If you need to add custom elements not supported by the template, you can edit the generated HTML directly. Some common additions:

- Custom diagrams or flowcharts
- Interactive elements
- Before/after comparisons

## Maintenance

The case study system is designed to be maintainable and scalable:

- To update the design system, edit the template files
- To update content, edit the JSON files and regenerate
- To add new sections to all case studies, update the template and generator script 