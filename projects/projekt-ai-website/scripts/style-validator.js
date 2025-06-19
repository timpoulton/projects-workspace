#!/usr/bin/env node

/**
 * PROJEKT AI STYLE VALIDATOR
 * Enforces Extra Medium design principles and catches style violations
 */

const fs = require('fs');
const path = require('path');

class StyleValidator {
    constructor() {
        this.violations = [];
        this.warnings = [];
        
        // Forbidden patterns
        this.forbiddenPatterns = {
            // Colors
            'blue': /(?:background|color|border).*?(?:#[0-9a-f]*[b-f][0-9a-f]*|blue|rgb\(\s*\d+\s*,\s*\d+\s*,\s*(?:1[5-9]\d|2\d\d)\s*\))/gi,
            'gradients': /(?:linear-gradient|radial-gradient|gradient)/gi,
            'bright-colors': /(?:#[0-9a-f]{2}[0-9a-f]{2}[0-9a-f]{2}|rgb\(\s*(?:1[5-9]\d|2[0-4]\d|25[0-5])\s*,\s*(?:1[5-9]\d|2[0-4]\d|25[0-5])\s*,\s*(?:1[5-9]\d|2[0-4]\d|25[0-5])\s*\))/gi,
            
            // Layout violations
            'rounded-corners': /border-radius\s*:\s*(?!0|50%)[^;]+/gi,
            'heavy-shadows': /box-shadow\s*:\s*[^;]*(?:\d{2,}px|\d+\.\d{2,})/gi,
            'complex-transforms': /transform\s*:\s*(?!translateY\(-?[0-5]px\))[^;]+/gi,
            
            // Typography violations
            'wrong-fonts': /font-family\s*:\s*(?!.*Inter)[^;]+/gi,
            'text-effects': /text-shadow|text-decoration(?!:\s*none)/gi,
            
            // Forbidden CSS files
            'legacy_css': /(?:portfolio-dark|style|dark-theme|extramedium-inspired|animations)\.css/gi
        };
        
        // Required patterns
        this.requiredPatterns = {
            'inter-font': /font-family.*Inter/gi,
            'proper-colors': /#(?:ffffff|f8f9fa|1a1a1a|666666|e9ecef)/gi
        };
        
        // Approved color palette
        this.approvedColors = [
            '#ffffff', '#fff',      // White
            '#f8f9fa',              // Light gray
            '#1a1a1a',              // Dark
            '#666666', '#666',      // Medium gray
            '#e9ecef',              // Border gray
            'white', 'black',       // Named colors
            'transparent', 'inherit'
        ];
    }
    
    validateFile(filePath) {
        if (!fs.existsSync(filePath)) {
            this.violations.push(`File not found: ${filePath}`);
            return;
        }
        
        const content = fs.readFileSync(filePath, 'utf8');
        const extension = path.extname(filePath);
        
        switch (extension) {
            case '.html':
                this.validateHTML(content, filePath);
                break;
            case '.css':
                this.validateCSS(content, filePath);
                break;
            case '.js':
                this.validateJS(content, filePath);
                break;
        }
    }
    
    validateHTML(content, filePath) {
        console.log(`🔍 Validating HTML: ${filePath}`);
        
        // Check for forbidden CSS imports
        if (this.forbiddenPatterns.legacy_css.test(content)) {
            this.violations.push(`${filePath}: Uses forbidden legacy CSS files`);
        }
        
        // Check inline styles for violations
        const inlineStyles = content.match(/style\s*=\s*["'][^"']*["']/gi) || [];
        inlineStyles.forEach(style => {
            this.validateInlineStyle(style, filePath);
        });
        
        // Check for proper structure
        if (!content.includes('Inter')) {
            this.warnings.push(`${filePath}: Inter font not detected`);
        }
        
        // Check for blue color violations
        if (this.forbiddenPatterns.blue.test(content)) {
            this.violations.push(`${filePath}: Contains forbidden blue colors`);
        }
        
        // Check for gradient usage
        if (this.forbiddenPatterns.gradients.test(content)) {
            this.violations.push(`${filePath}: Contains forbidden gradients`);
        }
    }
    
    validateCSS(content, filePath) {
        console.log(`🔍 Validating CSS: ${filePath}`);
        
        // Check each forbidden pattern
        Object.entries(this.forbiddenPatterns).forEach(([rule, pattern]) => {
            if (pattern.test(content)) {
                this.violations.push(`${filePath}: Violates rule "${rule}"`);
            }
        });
        
        // Check for approved colors only
        const colorMatches = content.match(/#[0-9a-f]{3,6}/gi) || [];
        colorMatches.forEach(color => {
            const normalizedColor = color.toLowerCase();
            if (!this.approvedColors.some(approved => 
                normalizedColor === approved.toLowerCase() || 
                normalizedColor === approved.toLowerCase().replace('#', '')
            )) {
                this.violations.push(`${filePath}: Uses non-approved color: ${color}`);
            }
        });
    }
    
    validateJS(content, filePath) {
        console.log(`🔍 Validating JS: ${filePath}`);
        
        // Check for inline style manipulation that might violate rules
        if (content.includes('style.background') && content.includes('blue')) {
            this.violations.push(`${filePath}: JavaScript modifies styles with blue colors`);
        }
        
        if (content.includes('gradient')) {
            this.violations.push(`${filePath}: JavaScript contains gradient references`);
        }
    }
    
    validateInlineStyle(styleAttr, filePath) {
        const styleContent = styleAttr.match(/["']([^"']*)["']/)[1];
        
        // Check for blue colors
        if (this.forbiddenPatterns.blue.test(styleContent)) {
            this.violations.push(`${filePath}: Inline style contains blue colors`);
        }
        
        // Check for gradients
        if (this.forbiddenPatterns.gradients.test(styleContent)) {
            this.violations.push(`${filePath}: Inline style contains gradients`);
        }
        
        // Check for improper border-radius
        if (this.forbiddenPatterns['rounded-corners'].test(styleContent)) {
            this.violations.push(`${filePath}: Inline style has improper border-radius`);
        }
    }
    
    scanDirectory(dirPath) {
        const files = fs.readdirSync(dirPath);
        
        files.forEach(file => {
            const fullPath = path.join(dirPath, file);
            const stat = fs.statSync(fullPath);
            
            if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
                this.scanDirectory(fullPath);
            } else if (stat.isFile() && /\.(html|css|js)$/.test(file)) {
                this.validateFile(fullPath);
            }
        });
    }
    
    generateReport() {
        console.log('\n' + '='.repeat(60));
        console.log('📋 PROJEKT AI STYLE VALIDATION REPORT');
        console.log('='.repeat(60));
        
        if (this.violations.length === 0 && this.warnings.length === 0) {
            console.log('✅ All files pass Extra Medium style validation!');
            return true;
        }
        
        if (this.violations.length > 0) {
            console.log('\n❌ STYLE VIOLATIONS FOUND:');
            this.violations.forEach((violation, index) => {
                console.log(`${index + 1}. ${violation}`);
            });
        }
        
        if (this.warnings.length > 0) {
            console.log('\n⚠️  WARNINGS:');
            this.warnings.forEach((warning, index) => {
                console.log(`${index + 1}. ${warning}`);
            });
        }
        
        console.log('\n📖 Review .cursorrules for complete style guidelines');
        console.log('='.repeat(60));
        
        return this.violations.length === 0;
    }
}

// Main execution
if (require.main === module) {
    const validator = new StyleValidator();
    const targetDir = process.argv[2] || '.';
    
    console.log('🚀 Starting Extra Medium Style Validation...');
    console.log(`📁 Scanning directory: ${path.resolve(targetDir)}`);
    
    validator.scanDirectory(targetDir);
    const passed = validator.generateReport();
    
    process.exit(passed ? 0 : 1);
}

module.exports = StyleValidator; 