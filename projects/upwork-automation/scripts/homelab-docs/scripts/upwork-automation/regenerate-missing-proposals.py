#!/usr/bin/env python3
"""
Regenerate Missing Proposal HTML Files
Creates HTML files for proposals that exist in queue but missing HTML files
"""

import json
import os
from datetime import datetime

QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
PROPOSALS_DIR = "/srv/apps/client-proposals/public/"
TEMPLATE_PATH = "/root/homelab-docs/projekt-ai-website/templates/dark-proposal-template.html"

def load_template():
    """Load the dark theme template"""
    try:
        with open(TEMPLATE_PATH, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading template: {e}")
        return None

def generate_html_from_proposal(proposal_data, template):
    """Generate HTML content from proposal data"""
    
    # Extract analysis data
    analysis = proposal_data.get('analysis', {})
    tools = analysis.get('tools', ['Automation Tools'])
    pain_points = analysis.get('pain_points', ['workflow optimization'])
    industry = analysis.get('industry', 'business')
    
    # Generate project title and subtitle
    project_title = f"Smart {industry.title()} Automation"
    project_subtitle = f"Transform your {pain_points[0]} with intelligent automation workflows"
    
    # Generate workflow steps
    workflow_steps = [
        {
            'title': 'Data Collection',
            'desc': 'Automatically capture and organize incoming data from your existing systems'
        },
        {
            'title': 'Smart Processing',
            'desc': f'Process information using {tools[0] if tools else "intelligent automation"} workflows'
        },
        {
            'title': 'Action Execution',
            'desc': 'Trigger appropriate actions and notifications based on predefined rules'
        },
        {
            'title': 'Results Tracking',
            'desc': 'Monitor performance and provide insights for continuous improvement'
        }
    ]
    
    # Generate process steps
    process_steps = [
        {
            'title': 'Discovery & Mapping',
            'desc': 'Analyze your current workflows and identify automation opportunities'
        },
        {
            'title': 'System Integration',
            'desc': f'Connect your existing tools with {tools[0] if tools else "automation platform"}'
        },
        {
            'title': 'Workflow Development',
            'desc': 'Build and test custom automation workflows tailored to your needs'
        },
        {
            'title': 'Training & Launch',
            'desc': 'Deploy the system and train your team for seamless adoption'
        }
    ]
    
    # Extract budget information
    budget = proposal_data.get('budget', 'Contact for pricing')
    price_range = extract_price_range(budget)
    delivery_weeks = estimate_delivery_time(analysis)
    
    # Replace template variables
    replacements = {
        '[CLIENT_NAME]': proposal_data.get('client_name', 'Valued Client'),
        '[PROJECT_TITLE]': project_title,
        '[PROJECT_SUBTITLE]': project_subtitle,
        '[SERVICE_1]': tools[0] if len(tools) > 0 else 'Automation Platform',
        '[SERVICE_2]': tools[1] if len(tools) > 1 else 'Integration Layer',
        '[SERVICE_3]': 'Custom Workflows',
        '[SERVICE_4]': 'Process Optimization',
        '[SERVICE_5]': 'Analytics & Monitoring',
        '[WORKFLOW_SUBTITLE]': f"Streamline your {industry} operations with smart automation",
        '[STEP_1_ICON]': '⚡',
        '[STEP_1_TITLE]': workflow_steps[0]['title'],
        '[STEP_1_DESC]': workflow_steps[0]['desc'],
        '[STEP_2_ICON]': '🔄',
        '[STEP_2_TITLE]': workflow_steps[1]['title'],
        '[STEP_2_DESC]': workflow_steps[1]['desc'],
        '[STEP_3_ICON]': '🎯',
        '[STEP_3_TITLE]': workflow_steps[2]['title'],
        '[STEP_3_DESC]': workflow_steps[2]['desc'],
        '[STEP_4_ICON]': '📊',
        '[STEP_4_TITLE]': workflow_steps[3]['title'],
        '[STEP_4_DESC]': workflow_steps[3]['desc'],
        '[STAT_1_VALUE]': '85',
        '[STAT_1_LABEL]': 'Time Saved',
        '[STAT_2_VALUE]': '99',
        '[STAT_2_LABEL]': 'Accuracy Rate',
        '[STAT_3_VALUE]': '24/7',
        '[STAT_3_LABEL]': 'Automation',
        '[CURRENT_PROCESS]': f"Currently handling {pain_points[0]} manually, leading to inefficiencies and potential errors.",
        '[DESIRED_OUTCOME]': f"Fully automated {industry} workflows that run seamlessly in the background, saving time and improving accuracy.",
        '[PROCESS_1_TITLE]': process_steps[0]['title'],
        '[PROCESS_1_DESC]': process_steps[0]['desc'],
        '[PROCESS_2_TITLE]': process_steps[1]['title'],
        '[PROCESS_2_DESC]': process_steps[1]['desc'],
        '[PROCESS_3_TITLE]': process_steps[2]['title'],
        '[PROCESS_3_DESC]': process_steps[2]['desc'],
        '[PROCESS_4_TITLE]': process_steps[3]['title'],
        '[PROCESS_4_DESC]': process_steps[3]['desc'],
        '[PRICE_RANGE]': price_range,
        '[DELIVERY_WEEKS]': delivery_weeks,
    }
    
    # Apply all replacements
    html_content = template
    for placeholder, value in replacements.items():
        html_content = html_content.replace(placeholder, str(value))
    
    return html_content

def extract_price_range(budget_text):
    """Extract meaningful price range from budget text"""
    
    budget_text = str(budget_text).lower()
    
    # Look for dollar amounts
    import re
    amounts = re.findall(r'\$(\d+(?:,\d{3})*)', budget_text)
    
    if amounts:
        # Convert to integers and find range
        amounts = [int(a.replace(',', '')) for a in amounts]
        if len(amounts) == 1:
            return f"${amounts[0]:,}"
        else:
            return f"${min(amounts):,} - ${max(amounts):,}"
    
    # Budget keywords mapping
    if any(word in budget_text for word in ['500', 'small', 'basic']):
        return "$500 - $1,500"
    elif any(word in budget_text for word in ['1000', '1500', 'medium']):
        return "$1,500 - $3,000"
    elif any(word in budget_text for word in ['3000', '5000', 'large']):
        return "$3,000 - $5,000"
    else:
        return "$1,500 - $3,000"  # Default

def estimate_delivery_time(analysis):
    """Estimate delivery time based on complexity"""
    
    score = analysis.get('score', 70)
    tools = analysis.get('tools', [])
    
    if score > 85 and len(tools) > 2:
        return "2-3 weeks"
    elif score > 70:
        return "3-4 weeks"
    else:
        return "4-6 weeks"

def regenerate_missing_proposals():
    """Regenerate missing proposal HTML files"""
    
    print("🔄 REGENERATING MISSING PROPOSAL HTML FILES")
    print()
    
    # Load template
    template = load_template()
    if not template:
        print("❌ Failed to load template")
        return
    
    # Load proposals from queue
    with open(QUEUE_FILE, 'r') as f:
        proposals = json.load(f)
    
    print(f"Found {len(proposals)} proposals in queue")
    
    regenerated_count = 0
    
    for proposal in proposals:
        filename = proposal.get('filename')
        if not filename:
            print(f"⚠️  Skipping proposal without filename: {proposal.get('job_title', 'Unknown')[:50]}...")
            continue
        
        filepath = os.path.join(PROPOSALS_DIR, filename)
        
        # Check if file already exists
        if os.path.exists(filepath):
            print(f"✅ Already exists: {filename}")
            continue
        
        # Generate HTML content
        html_content = generate_html_from_proposal(proposal, template)
        
        # Save HTML file
        try:
            os.makedirs(PROPOSALS_DIR, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(html_content)
            print(f"🆕 Generated: {filename}")
            regenerated_count += 1
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
    
    print(f"\n🎯 REGENERATED {regenerated_count} PROPOSAL HTML FILES")
    print(f"📁 Files saved to: {PROPOSALS_DIR}")
    print(f"🌐 All proposals now accessible via: https://proposals.projekt-ai.net/")

if __name__ == "__main__":
    regenerate_missing_proposals() 