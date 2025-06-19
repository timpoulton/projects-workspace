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
const { promisify } = require('util');
const readdir = promisify(fs.readdir);
const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);
const stat = promisify(fs.stat);

// Configuration
const rootDir = path.resolve(__dirname, '..');
const standardCssLinks = `
<link rel="stylesheet" href="/assets/css/main.css">
`;
const fontLinks = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">';

// Files or directories to skip
const skipPaths = [
  'node_modules',
  '.git',
  'venv',
  'archive',
  'backups'
];

// List of deprecated CSS files to remove references to
const deprecatedCssFiles = [
  'animations.css', 
  'portfolio-dark-theme.css',
  'style.css',
  'dark-theme.css',
  'portfolio.css',
  'extramedium-inspired.css',
  'admin.css',
  'apple-dark-style.css'
];

async function findAllHtmlFiles(dir) {
  const files = [];
  
  async function traverse(currentDir) {
    const entries = await readdir(currentDir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      const relativePath = path.relative(rootDir, fullPath);
      
      // Skip if path matches any in the skipPaths list
      if (skipPaths.some(skipPath => relativePath.startsWith(skipPath))) {
        continue;
      }
      
      if (entry.isDirectory()) {
        await traverse(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.html')) {
        files.push(fullPath);
      }
    }
  }
  
  await traverse(dir);
  return files;
}

async function fixHtmlFile(filePath) {
  try {
    console.log(`Processing ${path.relative(rootDir, filePath)}`);
    const content = await readFile(filePath, 'utf8');
    
    // Check if file needs updating
    const hasCssReferences = deprecatedCssFiles.some(cssFile => content.includes(cssFile)) ||
                            !content.includes('main.css') || 
                            content.includes('assets/css/style.css');
    
    if (!hasCssReferences) {
      console.log('  No changes needed');
      return false;
    }
    
    // Calculate path prefix based on file location relative to project root
    const relativePath = path.relative(rootDir, filePath);
    const depth = relativePath.split(path.sep).length - 1;
    const pathPrefix = depth > 0 ? '../'.repeat(depth) : '';
    
    // Replace deprecated CSS references with standardized version
    let updatedContent = content;
    
    // Remove deprecated CSS references
    deprecatedCssFiles.forEach(cssFile => {
      const regex = new RegExp(`<link[^>]*href="[^"]*${cssFile}"[^>]*>`, 'g');
      updatedContent = updatedContent.replace(regex, '');
    });
    
    // Replace all CSS paths with the correct relative paths
    const cssLinkRegex = /<link[^>]*rel="stylesheet"[^>]*href="[^"]*\/assets\/css\/([^"]+)"[^>]*>/g;
    updatedContent = updatedContent.replace(cssLinkRegex, (match, cssFile) => {
      return `<link rel="stylesheet" href="${pathPrefix}assets/css/${cssFile}">`;
    });
    
    // Add standard CSS if missing
    if (!updatedContent.includes('main.css')) {
      // Find head closing tag
      const headClosePos = updatedContent.indexOf('</head>');
      if (headClosePos !== -1) {
        const standardizedCssWithPrefix = standardCssLinks
          .replace(/\/assets\//g, `${pathPrefix}assets/`)
          .trim();
        
        // Add standardized CSS links before head close
        updatedContent = updatedContent.slice(0, headClosePos) + 
                        `\n  ${standardizedCssWithPrefix}\n  ` + 
                        updatedContent.slice(headClosePos);
      }
    }
    
    // Ensure we have the font link
    if (!updatedContent.includes('fonts.googleapis.com/css2?family=Inter')) {
      const headClosePos = updatedContent.indexOf('</head>');
      if (headClosePos !== -1) {
        updatedContent = updatedContent.slice(0, headClosePos) + 
                        `\n  ${fontLinks}\n  ` + 
                        updatedContent.slice(headClosePos);
      }
    }
    
    // Write updated content back to file
    if (content !== updatedContent) {
      await writeFile(filePath, updatedContent, 'utf8');
      console.log('  Updated CSS references');
      return true;
    } else {
      console.log('  No changes needed');
      return false;
    }
  } catch (err) {
    console.error(`Error processing ${filePath}:`, err);
    return false;
  }
}

async function main() {
  try {
    console.log('Finding HTML files...');
    const htmlFiles = await findAllHtmlFiles(rootDir);
    console.log(`Found ${htmlFiles.length} HTML files`);
    
    let updatedCount = 0;
    for (const filePath of htmlFiles) {
      const updated = await fixHtmlFile(filePath);
      if (updated) updatedCount++;
    }
    
    console.log(`Finished! Updated ${updatedCount} files.`);
  } catch (err) {
    console.error('Error:', err);
  }
}

main(); 