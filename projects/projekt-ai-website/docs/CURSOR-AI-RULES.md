# Cursor AI Rules for Projekt AI Website

## 🚨 CRITICAL DEPLOYMENT RULES

### 1. CSS STANDARDIZATION (MANDATORY)
- **ONLY USE THESE CSS FILES:**
  - `/assets/css/main.css` (global design system)
  - `/assets/css/case-study.css` (case study pages only)
- **NEVER REFERENCE:**
  - `portfolio-dark.css`
  - `style.css`
  - `dark-theme.css`
  - `extramedium-inspired.css`
  - `animations.css`
  - Any other legacy CSS files

### 2. DEPLOYMENT PROCESS (FOLLOW EXACTLY)
```bash
# Always run from project directory
cd /root/workspace/projects/projekt-ai-website

# Build before deploying
npm run build:prod

# Deploy to Netlify
netlify deploy --prod

# OR use git-based deployment
git add .
git commit -m "Descriptive commit message"
git push origin main
```

### 3. TEMPLATE HIERARCHY
- **Main homepage:** `index.html` (what users see at projekt-ai.net)
- **Test templates:** `index-extramedium-v2.html` (latest clean template)
- **Legacy templates:** Keep but don't modify without permission

## 🎯 DESIGN PRINCIPLES

### Visual Standards
- **Colors:** Black (#000), White (#fff), Gray (#666, #f8f8f8)
- **Typography:** Inter font family, clean hierarchy
- **Layout:** Generous whitespace, centered containers (max-width: 1400px)
- **No gradients:** Especially avoid blue gradients
- **Sharp corners:** No rounded elements unless specifically requested

### Content Structure
- **Hero Section:** Black background, white text, clear CTA
- **Services:** White background, card-based layout
- **Case Studies:** Grid layout with project previews
- **Contact:** Light gray background, centered content

## 📁 PROJECT STRUCTURE

### Key Directories
```
projects/projekt-ai-website/
├── assets/
│   ├── css/           # ONLY main.css and case-study.css
│   ├── img/           # Images and logos
│   └── js/            # JavaScript files
├── case-studies/      # Case study templates and data
├── services/          # Service pages
├── scripts/           # Build and maintenance scripts
└── docs/              # Documentation
```

### Content Organization
- **Services:** Located in `/services/` directory
- **Case Studies:** JSON data in `/case-studies/data/`
- **Assets:** Organized by type in `/assets/`

## 🛠️ COMMON TASKS

### Creating New Pages
```bash
# Use the page creation script
node scripts/create-new-page.js
```

### Fixing CSS References
```bash
# Clean up legacy CSS references
node scripts/fix-css-references.js
```

### Adding Case Studies
1. Create JSON file in `/case-studies/data/`
2. Use existing schema from `case-study-schema.json`
3. Generate HTML using templates

## ⚠️ TROUBLESHOOTING

### Changes Not Deploying
1. **Check build process:** Run `npm run build:prod`
2. **Verify main index.html:** Ensure it's updated, not just test templates
3. **Clear cache:** Browser cache may show old version
4. **Check Netlify logs:** Look for deployment errors

### CSS Not Loading
1. **Verify paths:** Use relative paths `/assets/css/main.css`
2. **Check build output:** Ensure CSS is copied to `dist/`
3. **Remove legacy references:** Use fix-css-references.js script

### Template Issues
1. **Start with clean template:** Use `index-extramedium-v2.html` as base
2. **Inline critical CSS:** For testing, put CSS in `<style>` tags
3. **Test locally:** Preview before deploying

## 🎨 BRAND GUIDELINES

### Voice & Tone
- **Professional but approachable**
- **Technical expertise without jargon**
- **Focus on ROI and business value**
- **Nightlife/entertainment industry focus**

### Content Themes
- **AI Automation for Nightlife**
- **Social Media Automation**
- **Marketing Automation**
- **Case Studies with Metrics**
- **ROI-focused messaging**

## 📊 PERFORMANCE STANDARDS

### Technical Requirements
- **Mobile-responsive design**
- **Fast loading times**
- **Clean, semantic HTML**
- **Optimized images**
- **Minimal JavaScript**

### SEO Considerations
- **Descriptive page titles**
- **Meta descriptions**
- **Proper heading hierarchy**
- **Alt text for images**
- **Clean URL structure**

## 🚫 WHAT NOT TO DO

### Never Do These:
1. **Don't add blue gradients** (user specifically dislikes them)
2. **Don't use legacy CSS files** (causes conflicts)
3. **Don't create rounded corners** without permission
4. **Don't deploy without testing** the main index.html
5. **Don't modify case study schema** without updating all files
6. **Don't add animations** unless specifically requested
7. **Don't create new CSS files** (use existing main.css)

### Avoid These Patterns:
- Complex animations (focus on layout)
- Multiple CSS files (consolidate)
- Inline styles (except for testing)
- Non-semantic HTML
- Overly complex JavaScript

## 🎯 SUCCESS METRICS

### Deployment Success
- [ ] Changes visible on live site (projekt-ai.net)
- [ ] No CSS conflicts or missing styles
- [ ] Mobile responsive
- [ ] Fast loading times
- [ ] No console errors

### Design Success
- [ ] Clean, professional appearance
- [ ] Matches requested design aesthetic
- [ ] Proper typography hierarchy
- [ ] Consistent spacing and alignment
- [ ] No blue gradients or unwanted styling

## 📞 ESCALATION

### When to Ask User
- **Major design changes**
- **New page creation**
- **Content strategy decisions**
- **Brand voice questions**
- **Technical architecture changes**

### When to Proceed
- **Bug fixes**
- **CSS cleanup**
- **Performance optimizations**
- **Mobile responsiveness fixes**
- **Content updates within existing structure**

---

**Remember:** The user has experienced frustration with changes not deploying and designs not matching expectations. Always verify your changes are working before claiming success, and be conservative with design decisions unless explicitly requested. 