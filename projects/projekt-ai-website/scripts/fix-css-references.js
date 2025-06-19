#!/usr/bin/env node

/**
 * CSS Reference Fixer
 * This script ensures all HTML files in the project use the correct CSS files
 * Based on the standard: 
 *   1. main.css (global design system)
 *   2. case-study.css (for case study pages only)
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// List of directories to process
const DIRECTORIES = [
  './',                    // Root HTML files
  './case-studies/',       // Case study pages
  './services/',           // Service pages
  './work/',               // Work pages
  './admin-dashboard/',    // Admin pages
  './projects/*/'          // Individual project pages
];

// List of CSS files to KEEP
const APPROVED_CSS = [
  'main.css',
  'case-study.css'
];

// List of CSS files to REMOVE (partial matches)
const DEPRECATED_CSS = [
  'portfolio-dark',
  'style.css',
  'dark-theme',
  'extramedium-inspired',
  'animations',
  'portfolio.css',
  'apple-dark-style'
];

// Counter for statistics
let stats = {
  filesProcessed: 0,
  filesUpdated: 0,
  cssRemoved: 0,
  errors: 0
};

/**
 * Fix CSS references in an HTML file
 */
function fixCssInFile(filePath) {
  try {
    console.log(`Processing: ${filePath}`);
    let content = fs.readFileSync(filePath, 'utf8');
    let originalContent = content;
    let cssCount = 0;
    
    // Match all CSS link elements
    const linkRegex = /<link[^>]*rel=["']stylesheet["'][^>]*href=["']([^"']+)["'][^>]*>/gi;
    const links = [];
    let match;
    
    // Collect all CSS links
    while ((match = linkRegex.exec(content)) !== null) {
      links.push({
        full: match[0],
        href: match[1]
      });
    }
    
    // Process each link
    links.forEach(link => {
      const cssFileName = path.basename(link.href);
      const cssPath = link.href;
      
      // Check if it's a deprecated CSS file
      const isDeprecated = DEPRECATED_CSS.some(deprecated => 
        cssFileName.includes(deprecated)
      );
      
      if (isDeprecated) {
        // Remove the link
        content = content.replace(link.full, '<!-- CSS removed by fix-css-references.js -->');
        cssCount++;
        console.log(`  Removed: ${cssFileName}`);
      }
    });
    
    // Find </head> tag
    const headEndIndex = content.indexOf('</head>');
    if (headEndIndex === -1) {
      console.error(`  Error: Could not find </head> tag in ${filePath}`);
      stats.errors++;
      return;
    }
    
    // Determine relative path to assets
    const relativePath = path.relative(path.dirname(filePath), './').replace(/\\/g, '/');
    const assetsPath = relativePath ? `${relativePath}/assets` : 'assets';
    
    // Check if required CSS files are present, add if not
    if (!content.includes('main.css')) {
      // Insert main.css before </head>
      const cssLink = `    <link rel="stylesheet" href="${assetsPath}/css/main.css">\n`;
      content = content.slice(0, headEndIndex) + cssLink + content.slice(headEndIndex);
      console.log(`  Added: main.css`);
    }
    
    // For case study pages, add case-study.css if needed
    if ((filePath.includes('case-stud') || filePath.includes('case_stud')) && 
        !content.includes('case-study.css')) {
      // Insert case-study.css before </head>
      const cssLink = `    <link rel="stylesheet" href="${assetsPath}/css/case-study.css">\n`;
      content = content.slice(0, headEndIndex) + cssLink + content.slice(headEndIndex);
      console.log(`  Added: case-study.css for case study page`);
    }
    
    // Save changes if content was modified
    if (content !== originalContent) {
      fs.writeFileSync(filePath, content, 'utf8');
      stats.filesUpdated++;
      stats.cssRemoved += cssCount;
      console.log(`  Updated file: ${filePath}`);
    }
    
    stats.filesProcessed++;
    
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error.message);
    stats.errors++;
  }
}

/**
 * Main function
 */
async function main() {
  console.log('\n🔍 CSS Reference Fixer\n');
  console.log('Scanning directories for HTML files...');
  
  // Process each directory
  for (const dir of DIRECTORIES) {
    try {
      // Get all HTML files in the directory
      const files = glob.sync(`${dir}*.html`);
      console.log(`\nFound ${files.length} HTML files in ${dir}`);
      
      // Process each file
      for (const file of files) {
        fixCssInFile(file);
      }
    } catch (error) {
      console.error(`Error processing directory ${dir}:`, error.message);
      stats.errors++;
    }
  }
  
  // Print summary
  console.log('\n📊 Summary:');
  console.log(`Files processed: ${stats.filesProcessed}`);
  console.log(`Files updated: ${stats.filesUpdated}`);
  console.log(`CSS references removed: ${stats.cssRemoved}`);
  console.log(`Errors encountered: ${stats.errors}`);
  
  if (stats.errors > 0) {
    console.log('\n⚠️ Some errors occurred. Please check the logs above.');
  } else {
    console.log('\n✅ CSS references have been fixed successfully!');
  }
}

// Execute main function
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
}); 