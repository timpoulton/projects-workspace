#!/usr/bin/env node

/**
 * Case Study Generator Script
 * This script generates HTML case study pages from JSON data files
 */

const fs = require('fs');
const path = require('path');

// Configuration
const DATA_DIR = path.join(__dirname, '../case-studies/data');
const TEMPLATE_PATH = path.join(__dirname, '../case-studies/template-extramedium.html');
const OUTPUT_DIR = path.join(__dirname, '../case-studies');

// Helper function to read JSON data
function readJsonData(filePath) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error reading JSON file ${filePath}:`, error);
    return null;
  }
}

// Helper function to read template
function readTemplate(templatePath) {
  try {
    return fs.readFileSync(templatePath, 'utf8');
  } catch (error) {
    console.error(`Error reading template file ${templatePath}:`, error);
    return null;
  }
}

// Generate HTML from template and JSON data
function generateHtml(template, data) {
  let html = template;
  
  // Replace basic fields
  html = html.replace(/{{CASE_TITLE}}/g, data.title || '');
  html = html.replace(/{{CASE_SUBTITLE}}/g, data.subtitle || '');
  html = html.replace(/{{CASE_DESCRIPTION}}/g, data.description || '');
  html = html.replace(/{{CASE_KEYWORDS}}/g, `${data.category}, ${data.industry}, Projekt AI, automation`);
  html = html.replace(/{{CASE_PREVIEW_IMAGE}}/g, data.featured_image || '');
  html = html.replace(/{{CLIENT_NAME}}/g, data.client_name || '');
  html = html.replace(/{{INDUSTRY}}/g, data.industry || '');
  html = html.replace(/{{SERVICES}}/g, data.services || '');
  html = html.replace(/{{YEAR}}/g, data.year || '');
  html = html.replace(/{{FEATURED_IMAGE}}/g, data.featured_image || '');
  html = html.replace(/{{OVERVIEW_TEXT}}/g, data.overview_text || '');
  
  // Challenge and solution
  html = html.replace(/{{CHALLENGE_TEXT}}/g, data.challenge?.text || '');
  html = html.replace(/{{SOLUTION_TEXT}}/g, data.solution?.text || '');
  
  // Challenge points
  let challengePoints = '';
  if (data.challenge && Array.isArray(data.challenge.points)) {
    challengePoints = data.challenge.points.map(point => `<li>${point}</li>`).join('\n');
  }
  html = html.replace(/{{CHALLENGE_POINTS}}/g, challengePoints);
  
  // Solution points
  let solutionPoints = '';
  if (data.solution && Array.isArray(data.solution.points)) {
    solutionPoints = data.solution.points.map(point => `<li>${point}</li>`).join('\n');
  }
  html = html.replace(/{{SOLUTION_POINTS}}/g, solutionPoints);
  
  // Process
  html = html.replace(/{{PROCESS_INTRO}}/g, data.process?.intro || '');
  
  // Process steps
  if (data.process && Array.isArray(data.process.steps)) {
    for (let i = 0; i < 4; i++) {
      const step = data.process.steps[i] || { title: '', text: '' };
      html = html.replace(`{{STEP_${i+1}_TITLE}}`, step.title || '');
      html = html.replace(`{{STEP_${i+1}_TEXT}}`, step.text || '');
    }
  }
  
  // Video info
  html = html.replace(/{{VIDEO_INTRO}}/g, data.video_info?.intro || '');
  html = html.replace(/{{VIDEO_SRC}}/g, data.video_info?.source || '');
  html = html.replace(/{{VIDEO_POSTER}}/g, data.video_info?.poster || '');
  html = html.replace(/{{VIDEO_CAPTION}}/g, data.video_info?.caption || '');
  
  // Results
  html = html.replace(/{{RESULTS_TEXT}}/g, data.results?.text || '');
  
  // Metrics
  if (data.results && Array.isArray(data.results.metrics)) {
    for (let i = 0; i < 3; i++) {
      const metric = data.results.metrics[i] || { value: '', label: '' };
      html = html.replace(`{{METRIC_${i+1}_VALUE}}`, metric.value || '');
      html = html.replace(`{{METRIC_${i+1}_LABEL}}`, metric.label || '');
    }
  }
  
  // Related projects
  if (data.related_projects && Array.isArray(data.related_projects)) {
    for (let i = 0; i < 3; i++) {
      const project = data.related_projects[i] || { title: '', url: '', image: '' };
      html = html.replace(`{{PROJECT_${i+1}_TITLE}}`, project.title || '');
      html = html.replace(`{{PROJECT_${i+1}_URL}}`, project.url || '');
      html = html.replace(`{{PROJECT_${i+1}_IMAGE}}`, project.image || '');
    }
  }
  
  return html;
}

// Process a single case study
function processCase(fileName) {
  const jsonPath = path.join(DATA_DIR, fileName);
  const data = readJsonData(jsonPath);
  
  if (!data || !data.id) {
    console.error(`Invalid JSON data in ${fileName}`);
    return false;
  }
  
  console.log(`Processing case study: ${data.id}`);
  
  const template = readTemplate(TEMPLATE_PATH);
  if (!template) return false;
  
  const html = generateHtml(template, data);
  const outputPath = path.join(OUTPUT_DIR, `${data.id}.html`);
  
  try {
    fs.writeFileSync(outputPath, html);
    console.log(`Generated: ${outputPath}`);
    return true;
  } catch (error) {
    console.error(`Error writing HTML file ${outputPath}:`, error);
    return false;
  }
}

// Main function
function main() {
  // Create output directory if it doesn't exist
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }
  
  // Get command line arguments
  const args = process.argv.slice(2);
  
  if (args.length > 0) {
    // Process specific files
    for (const arg of args) {
      if (!arg.endsWith('.json')) {
        processCase(`${arg}.json`);
      } else {
        processCase(arg);
      }
    }
  } else {
    // Process all JSON files in the data directory
    if (!fs.existsSync(DATA_DIR)) {
      console.error(`Data directory does not exist: ${DATA_DIR}`);
      process.exit(1);
    }
    
    const files = fs.readdirSync(DATA_DIR);
    const jsonFiles = files.filter(file => file.endsWith('.json'));
    
    console.log(`Found ${jsonFiles.length} case study data files`);
    
    let successful = 0;
    for (const file of jsonFiles) {
      if (processCase(file)) {
        successful++;
      }
    }
    
    console.log(`Successfully generated ${successful} out of ${jsonFiles.length} case studies`);
  }
}

// Run the script
main(); 