#!/usr/bin/env node

/**
 * New Page Generator
 * Creates new HTML pages with the correct CSS references
 */

const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const writeFile = promisify(fs.writeFile);
const mkdir = promisify(fs.mkdir);

// Get command line arguments
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node create-new-page.js <pageName> [--case-study]');
  process.exit(1);
}

const pageName = args[0];
const isCaseStudy = args.includes('--case-study');
const outputDir = path.dirname(pageName);
const outputPath = path.resolve(__dirname, '..', pageName);

// Create directory if it doesn't exist (for nested paths)
async function createDirectory(dirPath) {
  try {
    await mkdir(dirPath, { recursive: true });
    console.log(`Created directory: ${dirPath}`);
  } catch (err) {
    if (err.code !== 'EEXIST') {
      throw err;
    }
  }
}

// Determine how many levels deep the page is to set relative paths correctly
function getRelativePath(filePath) {
  const relativePath = path.relative(path.resolve(__dirname, '..'), path.dirname(filePath));
  const depth = relativePath === '' ? 0 : relativePath.split(path.sep).length;
  return depth > 0 ? '../'.repeat(depth) : '';
}

// Templates
function getStandardPageTemplate(relativePath) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Projekt AI</title>
  <meta name="description" content="Intelligent automation solutions for businesses">
  <link rel="icon" href="${relativePath}assets/img/logos/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="${relativePath}assets/css/main.css">
  <link rel="stylesheet" href="${relativePath}assets/css/extramedium.css">
</head>
<body>
  <header>
    <nav class="container">
      <a href="${relativePath}index.html" class="logo">Projekt<sup>AI</sup></a>
      <div class="nav-links">
        <a href="${relativePath}index.html">Home</a>
        <a href="${relativePath}services/index.html">Services</a>
        <a href="${relativePath}case-studies/index.html">Case Studies</a>
        <a href="${relativePath}index.html#contact">Contact</a>
      </div>
      <button class="menu-toggle">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </nav>
  </header>
  
  <main>
    <section class="section hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Your Page Title</h1>
          <p class="large-text">Your page description goes here. This template follows the Extra Medium design principles with clean, minimalist aesthetics.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2 class="section-title">Section Title</h2>
        <p>Section content goes here.</p>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <a href="${relativePath}index.html" class="logo">Projekt<sup>AI</sup></a>
        <div class="footer-links">
          <a href="${relativePath}index.html">Home</a>
          <a href="${relativePath}services/index.html">Services</a>
          <a href="${relativePath}case-studies/index.html">Case Studies</a>
          <a href="${relativePath}index.html#contact">Contact</a>
        </div>
      </div>
      <p>© ${new Date().getFullYear()} Projekt AI. All rights reserved.</p>
    </div>
  </footer>

  <div class="menu-overlay">
    <div class="slide-menu">
      <div class="menu-header">
        <a href="${relativePath}index.html" class="menu-logo">Projekt<sup>AI</sup></a>
        <button class="close-btn">&times;</button>
      </div>
      <nav class="menu-nav">
        <ul>
          <li><a href="${relativePath}index.html">Home</a></li>
          <li><a href="${relativePath}services/index.html">Services</a></li>
          <li><a href="${relativePath}case-studies/index.html">Case Studies</a></li>
          <li><a href="${relativePath}index.html#contact">Contact</a></li>
        </ul>
      </nav>
      <div class="menu-footer">
        <a href="mailto:hello@projekt-ai.net">hello@projekt-ai.net</a>
      </div>
    </div>
  </div>

  <script>
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const menuOverlay = document.querySelector('.menu-overlay');
    const slideMenu = document.querySelector('.slide-menu');
    const closeBtn = document.querySelector('.close-btn');

    menuToggle.addEventListener('click', () => {
      menuOverlay.classList.add('active');
      slideMenu.classList.add('active');
      menuToggle.classList.add('active');
    });

    closeBtn.addEventListener('click', () => {
      menuOverlay.classList.remove('active');
      slideMenu.classList.remove('active');
      menuToggle.classList.remove('active');
    });

    menuOverlay.addEventListener('click', (e) => {
      if (e.target === menuOverlay) {
        menuOverlay.classList.remove('active');
        slideMenu.classList.remove('active');
        menuToggle.classList.remove('active');
      }
    });
  </script>
</body>
</html>`;
}

function getCaseStudyTemplate(relativePath) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Case Study - Projekt AI</title>
  <meta name="description" content="Case study showcasing our automation solutions">
  <link rel="icon" href="${relativePath}assets/img/logos/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="${relativePath}assets/css/main.css">
  <link rel="stylesheet" href="${relativePath}assets/css/case-study.css">
</head>
<body>
  <header>
    <nav class="container">
      <a href="${relativePath}index.html" class="logo">Projekt<sup>AI</sup></a>
      <div class="nav-links">
        <a href="${relativePath}index.html">Home</a>
        <a href="${relativePath}services/index.html">Services</a>
        <a href="${relativePath}case-studies/index.html">Case Studies</a>
        <a href="${relativePath}index.html#contact">Contact</a>
      </div>
      <button class="menu-toggle">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </nav>
  </header>
  
  <section id="case-study-hero">
    <div class="container">
      <div class="back-link">
        <a href="${relativePath}case-studies/index.html">
          <svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 8H1m0 0l7 7M1 8l7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Back to Case Studies
        </a>
      </div>
      
      <div class="case-study-content">
        <div class="case-study-info">
          <div class="case-study-category">
            <span class="category-tag">Automation</span>
            <span class="industry-tag">Industry Name</span>
          </div>
          
          <h1>Case Study Title</h1>
          <p class="case-study-subtitle">Brief description of the project and its impact.</p>
          
          <div class="results-preview">
            <div class="result-stat">
              <span class="stat-number">85%</span>
              <span class="stat-label">Time Saved</span>
            </div>
            <div class="result-stat">
              <span class="stat-number">3x</span>
              <span class="stat-label">Output Increase</span>
            </div>
            <div class="result-stat">
              <span class="stat-number">100%</span>
              <span class="stat-label">Consistency</span>
            </div>
            <div class="result-stat">
              <span class="stat-number">24/7</span>
              <span class="stat-label">Availability</span>
            </div>
          </div>
        </div>
        
        <div class="case-study-visual">
          <div class="workflow-preview-large">
            <img src="${relativePath}assets/img/placeholder-workflow.png" alt="Workflow Diagram" class="hero-workflow-image">
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="problem-solution">
    <div class="container">
      <div class="problem-solution-grid">
        <div class="problem-section">
          <div class="section-icon">
            <i class="fas fa-exclamation-circle"></i>
          </div>
          <h2>The Challenge</h2>
          <p>Describe the problem the client was facing and why it needed a solution.</p>
          
          <div class="challenge-points">
            <div class="challenge-point">
              <i class="fas fa-times"></i>
              <div>
                <h4>Challenge Point 1</h4>
                <p>Description of this specific challenge.</p>
              </div>
            </div>
            <div class="challenge-point">
              <i class="fas fa-times"></i>
              <div>
                <h4>Challenge Point 2</h4>
                <p>Description of this specific challenge.</p>
              </div>
            </div>
            <div class="challenge-point">
              <i class="fas fa-times"></i>
              <div>
                <h4>Challenge Point 3</h4>
                <p>Description of this specific challenge.</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="solution-section">
          <div class="section-icon">
            <i class="fas fa-lightbulb"></i>
          </div>
          <h2>The Solution</h2>
          <p>Overview of the automation solution we implemented.</p>
          
          <div class="solution-points">
            <div class="solution-point">
              <i class="fas fa-check"></i>
              <div>
                <h4>Solution Point 1</h4>
                <p>Description of this aspect of the solution.</p>
              </div>
            </div>
            <div class="solution-point">
              <i class="fas fa-check"></i>
              <div>
                <h4>Solution Point 2</h4>
                <p>Description of this aspect of the solution.</p>
              </div>
            </div>
            <div class="solution-point">
              <i class="fas fa-check"></i>
              <div>
                <h4>Solution Point 3</h4>
                <p>Description of this aspect of the solution.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Add more sections as needed -->

  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <a href="${relativePath}index.html" class="logo">Projekt<sup>AI</sup></a>
        <div class="footer-links">
          <a href="${relativePath}index.html">Home</a>
          <a href="${relativePath}services/index.html">Services</a>
          <a href="${relativePath}case-studies/index.html">Case Studies</a>
          <a href="${relativePath}index.html#contact">Contact</a>
        </div>
      </div>
      <p>© ${new Date().getFullYear()} Projekt AI. All rights reserved.</p>
    </div>
  </footer>

  <div class="menu-overlay">
    <div class="slide-menu">
      <div class="menu-header">
        <a href="${relativePath}index.html" class="menu-logo">Projekt<sup>AI</sup></a>
        <button class="close-btn">&times;</button>
      </div>
      <nav class="menu-nav">
        <ul>
          <li><a href="${relativePath}index.html">Home</a></li>
          <li><a href="${relativePath}services/index.html">Services</a></li>
          <li><a href="${relativePath}case-studies/index.html">Case Studies</a></li>
          <li><a href="${relativePath}index.html#contact">Contact</a></li>
        </ul>
      </nav>
      <div class="menu-footer">
        <a href="mailto:hello@projekt-ai.net">hello@projekt-ai.net</a>
      </div>
    </div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
  <script>
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const menuOverlay = document.querySelector('.menu-overlay');
    const slideMenu = document.querySelector('.slide-menu');
    const closeBtn = document.querySelector('.close-btn');

    menuToggle.addEventListener('click', () => {
      menuOverlay.classList.add('active');
      slideMenu.classList.add('active');
      menuToggle.classList.add('active');
    });

    closeBtn.addEventListener('click', () => {
      menuOverlay.classList.remove('active');
      slideMenu.classList.remove('active');
      menuToggle.classList.remove('active');
    });

    menuOverlay.addEventListener('click', (e) => {
      if (e.target === menuOverlay) {
        menuOverlay.classList.remove('active');
        slideMenu.classList.remove('active');
        menuToggle.classList.remove('active');
      }
    });
  </script>
</body>
</html>`;
}

// Main function
async function main() {
  try {
    // Create directory for the file if needed
    if (outputDir && outputDir !== '.') {
      await createDirectory(path.dirname(outputPath));
    }
    
    // Calculate relative path
    const relativePath = getRelativePath(outputPath);
    
    // Select appropriate template
    const template = isCaseStudy 
      ? getCaseStudyTemplate(relativePath) 
      : getStandardPageTemplate(relativePath);
    
    // Write the file
    await writeFile(outputPath, template, 'utf8');
    
    console.log(`✅ Created new ${isCaseStudy ? 'case study ' : ''}page: ${outputPath}`);
    console.log(`   with correct styling and relative paths`);
    
  } catch (error) {
    console.error(`Error creating page:`, error);
    process.exit(1);
  }
}

main(); 