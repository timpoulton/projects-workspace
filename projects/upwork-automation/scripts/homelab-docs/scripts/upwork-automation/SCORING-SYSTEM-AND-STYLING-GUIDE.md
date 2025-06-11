# Upwork Automation Scoring System & Dark Theme Styling Guide

## 🎯 Understanding the Scoring System

The scoring system is designed to filter and prioritize Upwork jobs based on automation relevance and your expertise. Here's how it works:

### Scoring Categories

1. **🔴 MUST APPLY (80+ points)**
   - Premium opportunities that match your expertise perfectly
   - Typically include multiple automation keywords and high budgets
   - AI generates comprehensive, detailed proposals

2. **🟡 SHOULD APPLY (60-79 points)**
   - Good opportunities worth pursuing
   - Solid automation projects with decent budgets
   - AI generates professional standard proposals

3. **🟢 CONSIDER (40-59 points)**
   - Opportunities that might be worth exploring
   - Basic automation needs or lower budgets
   - AI generates concise, focused proposals

4. **❌ SKIP (<40 points)**
   - Jobs that don't meet minimum criteria
   - Rejected automatically by the system

### How Scoring Works

The system evaluates jobs based on multiple factors:

#### 1. **Automation Requirements** (CRITICAL)
- **Minimum 2 automation terms required** from approved list
- Terms include: automation, automate, workflow, integration, api, webhook, make.com, zapier, n8n, etc.
- Jobs without enough automation terms are **immediately rejected**

#### 2. **Budget Scoring** (0-40 points)
```
- Enterprise ($10k+): 40 points
- High ($5k-$9,999): 35 points
- Good ($3k-$4,999): 30 points
- Medium ($2k-$2,999): 25 points
- Low-Medium ($1k-$1,999): 20 points
- Low ($500-$999): 10 points
- Minimal (<$500): 5 points
```

#### 3. **Keyword Bonuses**
- **AI Automation** (35 points): ai agent, chatbot, ai workflow
- **Primary Tools** (30 points): make.com, n8n, zapier
- **Your Specialties** (25 points): webflow, social media automation
- **General Automation** (20 points): automation, workflow, integration

#### 4. **Negative Keywords** (Immediate Disqualifiers)
- Virtual assistant, VA needed, data entry only
- Frontend/backend developer positions
- WordPress/Shopify only projects
- Manual work with no automation

#### 5. **Client Quality** (up to 55 points)
- Enterprise client ($100k+ spent): 25 points
- Payment verified: 10 points
- High hire rate (80%+): 10 points
- Good rating (4.8+): 10 points

### Why Jobs Are Being Rejected

Common reasons for rejection:
1. **Not enough automation terms** - Job must have at least 2 automation-related keywords
2. **Disqualifier keywords** - Contains terms like "virtual assistant" or "developer needed"
3. **Below minimum score** - Total score less than 40 points
4. **Budget too low** - Below $800 minimum

## 🎨 Dark Theme Styling Implementation

To match the projekt-ai.net aesthetic, here's the complete styling system:

### Color Palette
```css
:root {
  /* Background Colors */
  --bg-primary: #0a0a0a;        /* Main background */
  --bg-secondary: #1a1a1a;      /* Card backgrounds */
  --bg-hover: rgba(255, 255, 255, 0.03);
  
  /* Text Colors */
  --text-primary: #ffffff;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --text-muted: rgba(255, 255, 255, 0.5);
  
  /* Border Colors */
  --border-primary: rgba(255, 255, 255, 0.08);
  --border-hover: rgba(255, 255, 255, 0.12);
  
  /* Status Colors */
  --success: #4CAF50;
  --warning: #FFC107;
  --info: #2196F3;
  --danger: #F44336;
  
  /* Accent Colors */
  --accent-primary: #6C63FF;    /* Upwork purple */
}
```

### Typography
```css
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-primary);
  background: var(--bg-primary);
}

h1, h2, h3 {
  font-weight: 700;
  letter-spacing: -0.02em;
}
```

### Card Component
```css
.job-card {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 30px;
  transition: all 0.3s ease;
}

.job-card:hover {
  background: rgba(255, 255, 255, 0.03);
  border-color: rgba(255, 255, 255, 0.12);
  transform: translateY(-2px);
}
```

### Score Badges
```css
.score-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.score-must {
  background: rgba(76, 175, 80, 0.15);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.score-should {
  background: rgba(255, 193, 7, 0.15);
  color: #FFC107;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.score-consider {
  background: rgba(33, 150, 243, 0.15);
  color: #2196F3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}
```

### Action Buttons
```css
.action-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  background: transparent;
  color: rgba(255, 255, 255, 0.8);
}

.btn-generate {
  background: rgba(108, 99, 255, 0.1);
  border-color: rgba(108, 99, 255, 0.3);
  color: #6C63FF;
}

.btn-generate:hover {
  background: rgba(108, 99, 255, 0.2);
  border-color: rgba(108, 99, 255, 0.5);
}

.btn-reject {
  background: rgba(244, 67, 54, 0.1);
  border-color: rgba(244, 67, 54, 0.3);
  color: #F44336;
}

.btn-reject:hover {
  background: rgba(244, 67, 54, 0.2);
  border-color: rgba(244, 67, 54, 0.5);
}
```

### Glass Morphism Effects
```css
.glass-card {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}
```

## 🔧 Implementation in Simple Generator

To implement this styling in your simple generator, update the template in `simple-upwork-generator.py`:

```python
# In the main page template
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Apply the dark theme variables and styles from above */
    /* ... (include all the CSS from the styling section) ... */
</style>
```

### Job Display Template
```html
<div class="job-card" data-job-id="{{ job.job_id }}">
    <div class="job-header">
        <div>
            <h3 class="job-title">{{ job.job_title }}</h3>
            <p class="job-client">{{ job.client_name }}</p>
        </div>
        <div class="job-score">
            <span class="score-badge {{ score_class }}">{{ score_category }}</span>
            <span class="score-value">{{ job.score }}</span>
        </div>
    </div>
    
    <p class="job-description">{{ job.description[:200] }}...</p>
    
    <div class="job-meta">
        <span>💰 {{ job.budget }}</span>
        <span>📅 {{ job.created_at }}</span>
        <span>🤖 {{ job.automation_terms_found }} automation terms</span>
    </div>
    
    <div class="job-actions">
        <button class="action-btn btn-generate" onclick="generateProposal('{{ job.job_id }}')">
            ✨ Generate Proposal
        </button>
        <button class="action-btn btn-reject" onclick="rejectJob('{{ job.job_id }}')">
            ❌ Reject
        </button>
    </div>
</div>
```

## 📊 Debugging Scoring Issues

If jobs are being rejected unexpectedly:

1. **Check the logs** for scoring details:
   ```bash
   tail -f simple-generator.log | grep -E "(ADVANCED SCORING|automation terms|score)"
   ```

2. **Verify automation terms** in the job:
   - Must have at least 2 terms from the approved list
   - Check `scoring-config.json` for the full list

3. **Look for disqualifiers**:
   - Search for "virtual assistant", "VA needed", etc.
   - These immediately reject the job regardless of score

4. **Test with known good job**:
   ```python
   # Use the test script with automation keywords
   job_data = {
       'job_title': 'Automate Restaurant Inventory with Make.com',
       'description': 'Need automation expert to integrate our POS with inventory system using Make.com workflows',
       'budget': '$3000',
       'client_name': 'Restaurant Group'
   }
   ```

## 🚀 Next Steps

1. **Update your simple generator** with the dark theme styling
2. **Monitor the scoring** to ensure relevant jobs aren't rejected
3. **Adjust scoring weights** in `scoring-config.json` if needed
4. **Test with real jobs** from the Chrome extension

The scoring system is designed to be strict to ensure only high-quality automation opportunities are pursued. If you're seeing too many rejections, consider adjusting the `min_automation_score` or `minimum_required` automation terms in the configuration. 