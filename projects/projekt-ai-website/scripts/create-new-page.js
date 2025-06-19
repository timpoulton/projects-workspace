#!/usr/bin/env node

/**
 * New Page Generator
 * Creates new HTML pages with the correct CSS references
 */

const fs = require('fs');
const path = require('path');

// Template for new pages
const PAGE_TEMPLATE = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{PAGE_TITLE}} | Projekt AI</title>
    
    <!-- Meta information -->
    <meta name="description" content="{{PAGE_DESCRIPTION}}">
    <meta name="author" content="Projekt AI">
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Core stylesheets only -->
    <link rel="stylesheet" href="{{RELATIVE_PATH}}assets/css/main.css">
    {{CASE_STUDY_CSS}}
</head>
<body>
    <!-- HEADER -->
    <header>
        <nav>
            <div class="logo">Projekt<span>AI</span></div>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/services/">Services</a></li>
                <li><a href="/index.html#contact">Contact</a></li>
            </ul>
            <div class="nav-buttons">
                <a href="#cta" class="btn btn-primary">Get Blueprint</a>
            </div>
        </nav>
    </header>

    <!-- MAIN CONTENT -->
    <section class="hero">
        <div class="container">
            <h1>{{PAGE_TITLE}}</h1>
            <p>{{PAGE_DESCRIPTION}}</p>
        </div>
    </section>

    <section class="content-section">
        <div class="container">
            <h2>Content Title</h2>
            <p>Add your content here.</p>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
        <div class="container footer-content">
            <p>© 2025 Projekt AI</p>
            <div class="footer-links">
                <a href="/index.html#about">About</a>
                <a href="/index.html#contact">Contact</a>
            </div>
        </div>
    </footer>
</body>
</html>`;

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 2) {
    console.error('Usage: node create-new-page.js <output-file> <page-title> [page-description] [is-case-study]');
    console.error('Example: node create-new-page.js ./case-studies/new-case.html "New Case Study" "Description" true');
    process.exit(1);
}

const outputFile = args[0];
const pageTitle = args[1];
const pageDescription = args[2] || 'Projekt AI - Automation Solutions for Music and Hospitality';
const isCaseStudy = args[3] === 'true';

// Ensure output directory exists
const outputDir = path.dirname(outputFile);
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    console.log(`Created directory: ${outputDir}`);
}

// Calculate relative path to assets
const relativePath = path.relative(outputDir, './').replace(/\\/g, '/');
const relativeTo = relativePath ? `${relativePath}/` : '';

// Generate the HTML content
let html = PAGE_TEMPLATE
    .replace(/{{PAGE_TITLE}}/g, pageTitle)
    .replace(/{{PAGE_DESCRIPTION}}/g, pageDescription)
    .replace(/{{RELATIVE_PATH}}/g, relativeTo);

// Add case-study.css if needed
if (isCaseStudy) {
    html = html.replace('{{CASE_STUDY_CSS}}', `<link rel="stylesheet" href="${relativeTo}assets/css/case-study.css">`);
} else {
    html = html.replace('{{CASE_STUDY_CSS}}', '');
}

// Write the file
fs.writeFileSync(outputFile, html, 'utf8');
console.log(`Created new page at: ${outputFile}`);
console.log(`Title: ${pageTitle}`);
console.log(`CSS References: main.css${isCaseStudy ? ' and case-study.css' : ''}`);

console.log('\n✅ Page created successfully!');
console.log('To add custom content, edit the file in your text editor.'); 