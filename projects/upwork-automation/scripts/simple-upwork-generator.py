#!/usr/bin/env python3
"""
Simple Upwork Proposal Generator
A streamlined version that:
1. Receives job data from Chrome extension via webhook
2. Uses the existing Multi-Model AI to generate proposals
3. Displays jobs and proposals in a web interface
"""

import flask
from flask import Flask, request, render_template_string, jsonify, redirect
import requests
import re
import json
import os
import datetime
import html
import uuid
import logging
import sys
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('simple-generator.log')
    ]
)
logger = logging.getLogger('simple-upwork-generator')

# Configuration
PORT = 5056  # Different port to avoid conflicts
MULTIMODEL_SERVER = "http://localhost:5002"  # Existing Multi-Model AI server
DARK_THEME_TEMPLATE_PATH = os.environ.get("DARK_THEME_TEMPLATE_PATH", "/var/www/projekt-ai.net/templates/dark-proposal-template.html")
FALLBACK_TEMPLATE_PATH = "/root/homelab-docs/scripts/upwork-automation/proposal-template.html"
QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"

# Initialize Flask app
app = Flask(__name__)

logger.info(f"🚀 Starting Simple Upwork Proposal Generator on port {PORT}")
logger.info(f"📊 Using Multi-Model AI Server at {MULTIMODEL_SERVER}")
logger.info(f"🌐 Open your browser to http://localhost:{PORT}")
logger.info(f"🔗 Chrome Extension Webhook: http://192.168.1.107:{PORT}/webhook/rss-jobs")

# Load the queue file
def load_queue():
    """Load the proposal queue from file"""
    try:
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"Error loading queue: {e}")
        return []

# Save the queue file
def save_queue(queue):
    """Save the proposal queue to file"""
    try:
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving queue: {e}")
        return False

# Load the dark theme template
def load_template():
    """Load the dark theme template file, falling back to a simpler one if not available"""
    if os.path.exists(DARK_THEME_TEMPLATE_PATH):
        with open(DARK_THEME_TEMPLATE_PATH, 'r') as f:
            return f.read()
    elif os.path.exists(FALLBACK_TEMPLATE_PATH):
        with open(FALLBACK_TEMPLATE_PATH, 'r') as f:
            return f.read()
    else:
        # Basic fallback template
        return """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{job_title}} - Proposal</title>
            <style>
                body { font-family: 'Inter', sans-serif; background: #121212; color: #eee; }
                .container { max-width: 800px; margin: 0 auto; padding: 20px; }
                .header { border-bottom: 1px solid #333; padding-bottom: 20px; margin-bottom: 20px; }
                .section { margin: 20px 0; background: #1e1e1e; padding: 20px; border-radius: 8px; }
                pre { white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{{job_title}}</h1>
                    <p>Client: {{client_name}} | Budget: {{budget}}</p>
                </div>
                <div class="section">
                    <h2>Job Description</h2>
                    <pre>{{description}}</pre>
                </div>
                <div class="section">
                    <h2>Generated Proposal</h2>
                    <pre>{{message}}</pre>
                </div>
                <div class="section">
                    <h2>Analysis</h2>
                    <p><strong>Industry:</strong> {{industry}}</p>
                    <p><strong>Pain Points:</strong> {{pain_points}}</p>
                    <p><strong>Score:</strong> {{score}}</p>
                </div>
                <div style="text-align: center; margin-top: 20px; opacity: 0.6;">
                    Generated {{timestamp}}
                </div>
            </div>
        </body>
        </html>"""

# Extract Upwork job details from URL
def extract_job_details(url):
    """
    Extract essential job details from an Upwork job URL using requests
    """
    logger.info(f"Extracting job details from URL: {url}")
    
    try:
        # Use a proper User-Agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        content = response.text
        
        # Extract job title
        title_match = re.search(r'<title>(.*?)</title>', content)
        job_title = title_match.group(1).replace(' | Upwork', '') if title_match else "Unknown Job"
        
        # Extract job description
        desc_match = re.search(r'<div class="up-card-section up-card-section-margin[^"]*?">.*?<span[^>]*?>(.*?)</div>\\s*</div>', content, re.DOTALL)
        description = desc_match.group(1) if desc_match else "Description not found"
        
        # Clean up HTML
        description = re.sub(r'<[^>]*>', ' ', description)
        description = re.sub(r'\s+', ' ', description)
        description = html.unescape(description)
        
        # Extract budget
        budget_match = re.search(r'Budget:</dt>\\s*<dd[^>]*>([^<]*)</dd>', content)
        budget = budget_match.group(1).strip() if budget_match else "Not specified"
        
        # Extract client name
        client_match = re.search(r'client-name[^>]*>([^<]*)</span>', content)
        client_name = client_match.group(1).strip() if client_match else "Client"
        
        logger.info(f"Successfully extracted job details using requests: {job_title}")
        return {
            "job_title": job_title,
            "description": description,
            "budget": budget,
            "client_name": client_name,
            "url": url
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            logger.error(f"Access forbidden (403) when trying to access Upwork. They may be blocking automated access.")
            # Return minimal info to allow manual entry
            return {
                "job_title": "Could not access Upwork job (403 Forbidden)",
                "description": "Upwork is blocking automated access. Please enter details manually.",
                "budget": "Unknown",
                "client_name": "Unknown",
                "url": url,
                "extraction_failed": True
            }
        else:
            logger.error(f"HTTP error extracting job details: {e}")
            return {
                "job_title": f"Error extracting job details: HTTP {e.response.status_code}",
                "description": f"Failed to extract job details: {str(e)}",
                "budget": "Unknown",
                "client_name": "Unknown",
                "url": url,
                "extraction_failed": True
            }
    except Exception as e:
        logger.error(f"Error extracting job details: {e}")
        return {
            "job_title": "Error extracting job details",
            "description": f"Failed to extract job details: {str(e)}",
            "budget": "Unknown",
            "client_name": "Unknown",
            "url": url,
            "extraction_failed": True
        }

# Generate proposal using the existing Multi-Model AI
def generate_proposal(job_details):
    """
    Generate a proposal using the Multi-Model AI server
    """
    logger.info(f"Generating proposal for job: {job_details['job_title']}")
    try:
        # Send job details to the AI server
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{MULTIMODEL_SERVER}/webhook/job-direct", json=job_details, headers=headers)
        response.raise_for_status()
        ai_response = response.json()
        logger.info(f"AI server response: {ai_response}")  # Log the AI server response

        # Check if the response contains the expected data
        message = ai_response.get('message')
        if not message and 'proposal_sections' in ai_response:
            message = ai_response['proposal_sections'].get('automated_solution')

        if not message:
            logger.warning("AI server did not return a valid message in the response.")
            return None

        ai_response['message'] = message  # Ensure downstream code can use ai_response['message']

        return ai_response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with AI server: {e}")
        return None
    except ValueError as e:
        logger.error(f"Error parsing AI server response: {e}")
        return None

# Format proposal with template
def format_proposal_with_template(proposal_data):
    """
    Format the proposal data using the dark theme template
    """
    logger.info(f"Formatting proposal for job: {proposal_data.get('job_title', 'Unknown')}")
    logger.info(f"Proposal data keys: {list(proposal_data.keys())}")
    logger.info(f"Message exists: {'message' in proposal_data}")
    logger.info(f"Message length: {len(proposal_data.get('message', ''))}")
    
    try:
        template = load_template()
        
        # Replace placeholders in template with actual data
        formatted = template
        
        # Basic replacements with safe defaults - Using square brackets format [PLACEHOLDER]
        formatted = formatted.replace('[CLIENT_NAME]', proposal_data.get('client_name', 'Client'))
        formatted = formatted.replace('[PROJECT_TITLE]', proposal_data.get('job_title', 'Project'))
        formatted = formatted.replace('[PROJECT_TYPE]', 'Automation')
        formatted = formatted.replace('[PROJECT_SUBTITLE]', proposal_data.get('description', '').split('.')[:2][0] if proposal_data.get('description') else proposal_data.get('job_title', 'Custom Solution'))
        formatted = formatted.replace('[JOB_BUDGET]', proposal_data.get('budget', 'Not specified'))
        formatted = formatted.replace('[SCORE]', str(proposal_data.get('score', 75)))
        
        # Handle URL - make sure it's always present
        job_url = proposal_data.get('original_job_url', 
                 proposal_data.get('url', 
                 proposal_data.get('job_url', '#')))
        
        logger.debug(f"Using job URL: {job_url}")
        formatted = formatted.replace('[ORIGINAL_JOB_URL]', job_url)
        
        # Analysis data
        analysis = proposal_data.get('analysis', {})
        industry = analysis.get('industry', 'Business')
        pain_points = ', '.join(analysis.get('pain_points', ['manual processes']))
        tools = ', '.join(analysis.get('tools', ['Automation Tools']))
        
        # Use the actual message from the AI
        message = proposal_data.get('message', 'I can help you achieve your goals with a custom solution.')
        logger.info(f"Using AI message: {message[:100]}...")
        
        # Dynamic mapping of proposal sections
        sections = proposal_data.get('proposal_sections', {})
        # Services
        techs = [t.strip() for t in sections.get('technologies_used', '').split(',') if t.strip()]
        for idx in range(1, 6):
            formatted = formatted.replace(f'[SERVICE_{idx}]', techs[idx-1] if idx-1 < len(techs) else '')
        # Challenge section
        formatted = formatted.replace('[CURRENT_PROCESS]', sections.get('current_process', ''))
        formatted = formatted.replace('[DESIRED_OUTCOME]', sections.get('automated_solution', ''))
        # Process/Technical Roadmap
        roadmap = sections.get('technical_roadmap', '')
        # Fix: Avoid look-behind, split on start or whitespace + number + dot
        roadmap_steps = re.split(r'(?:^|\s)\d+\.', roadmap)
        roadmap_steps = [s.strip() for s in roadmap_steps if s.strip()]
        for idx in range(1, 5):
            formatted = formatted.replace(f'[PROCESS_{idx}_TITLE]', f'Step {idx}')
            formatted = formatted.replace(f'[PROCESS_{idx}_DESC]', roadmap_steps[idx-1] if idx-1 < len(roadmap_steps) else '')
        
        # Workflow steps
        workflow = sections.get('automated_workflow', '')
        # Fix: Avoid look-behind, split on start or whitespace + number + dot
        wf_steps = re.split(r'(?:^|\s)\d+\.', workflow)
        wf_steps = [s.strip() for s in wf_steps if s.strip()]
        for idx in range(1, 5):
            formatted = formatted.replace(f'[STEP_{idx}_TITLE]', f'Step {idx}')
            formatted = formatted.replace(f'[STEP_{idx}_DESC]', wf_steps[idx-1] if idx-1 < len(wf_steps) else '')
            formatted = formatted.replace(f'[STEP_{idx}_ICON]', '⚡')
        # Remove any remaining placeholders
        formatted = re.sub(r'\[[A-Z_]+\]', '', formatted)
        
        # Statistics
        formatted = formatted.replace('[STAT_1_VALUE]', '80')
        formatted = formatted.replace('[STAT_1_LABEL]', 'Time Saved')
        formatted = formatted.replace('[STAT_2_VALUE]', '95')
        formatted = formatted.replace('[STAT_2_LABEL]', 'Accuracy Rate')
        formatted = formatted.replace('[STAT_3_VALUE]', '24')
        formatted = formatted.replace('[STAT_3_LABEL]', 'Hours/Week Freed')
        
        # Investment section
        formatted = formatted.replace('[PRICE_RANGE]', proposal_data.get('budget', '$2,500 - $5,000'))
        formatted = formatted.replace('[DELIVERY_WEEKS]', '2-3 weeks')
        
        # Main content replacement - This is the most important one
        formatted = formatted.replace('[PROPOSED_SOLUTION]', message)
        formatted = formatted.replace('[PROJECT_DESCRIPTION]', proposal_data.get('description', message))
        formatted = formatted.replace('[ANALYSIS_CONTENT]', f"Analysis for {industry} automation: {message}")
        
        # Technical details
        formatted = formatted.replace('[TECHNICAL_DETAILS]', f"Technical implementation using {tools} that integrates with your existing systems.")
        formatted = formatted.replace('[IMPLEMENTATION_APPROACH]', message)
        
        # Timeline and deliverables
        formatted = formatted.replace('[TIMELINE]', "7-14 days depending on complexity")
        formatted = formatted.replace('[DELIVERABLES]', "Complete automation solution, documentation, training materials, and 30 days support")
        
        # Remove any remaining placeholders that weren't replaced
        formatted = re.sub(r'\[[A-Z_]+\]', '', formatted)
        
        # Also handle double curly braces for backwards compatibility
        formatted = formatted.replace('{{CLIENT_NAME}}', proposal_data.get('client_name', 'Client'))
        formatted = formatted.replace('{{JOB_TITLE}}', proposal_data.get('job_title', 'Job'))
        formatted = formatted.replace('{{JOB_BUDGET}}', proposal_data.get('budget', 'Not specified'))
        formatted = formatted.replace('{{SCORE}}', str(proposal_data.get('score', 75)))
        formatted = formatted.replace('{{ORIGINAL_JOB_URL}}', job_url)
        formatted = formatted.replace('{{TIMESTAMP}}', proposal_data.get('timestamp', proposal_data.get('created_at', datetime.datetime.now().isoformat())))
        formatted = formatted.replace('{{PROPOSED_SOLUTION}}', message)
        formatted = formatted.replace('{{message}}', message)
        formatted = formatted.replace('{{description}}', proposal_data.get('description', message))
        formatted = formatted.replace('{{client_name}}', proposal_data.get('client_name', 'Client'))
        formatted = formatted.replace('{{job_title}}', proposal_data.get('job_title', 'Job'))
        formatted = formatted.replace('{{budget}}', proposal_data.get('budget', 'Not specified'))
        formatted = formatted.replace('{{industry}}', industry)
        formatted = formatted.replace('{{pain_points}}', pain_points)
        formatted = formatted.replace('{{score}}', str(proposal_data.get('score', 75)))
        
        # Remove any remaining double curly braces
        formatted = re.sub(r'\{\{[A-Z_a-z]+\}\}', '', formatted)
        
        # Use location/country for client label if available
        client_location = proposal_data.get('client_location') or proposal_data.get('country') or proposal_data.get('client_name', 'Client')
        logger.info(f"Using client label: {client_location}")
        formatted = formatted.replace('[CLIENT_NAME]', client_location)
        # For job subtitle/summary, use a concise summary of the job description
        job_description = proposal_data.get('description', '')
        summary_sentences = job_description.split('.')[:2]
        summary = '. '.join([s.strip() for s in summary_sentences if s.strip()])
        if summary and not summary.endswith('.'):
            summary += '.'
        logger.info(f"Using job summary for subtitle: {summary}")
        formatted = formatted.replace('[PROJECT_SUBTITLE]', summary or proposal_data.get('job_title', 'Custom Solution'))
        
        logger.info(f"Successfully formatted proposal with actual AI content")
        return formatted
    except Exception as e:
        logger.error(f"Error formatting proposal: {e}")
        # Return a simple error page if formatting fails
        return f"""<!DOCTYPE html>
        <html>
        <head><title>Error Formatting Proposal</title></head>
        <body style="background: #1a1a1a; color: white; padding: 20px;">
            <h1>Error Formatting Proposal</h1>
            <p>An error occurred while formatting the proposal: {str(e)}</p>
            <p>AI Message: {proposal_data.get('message', 'No message available')}</p>
            <p>Please try again or contact support.</p>
        </body>
        </html>"""

# Routes
@app.route('/')
def index():
    """
    Main page showing jobs from Chrome extension
    """
    # Load available jobs from the queue file
    available_jobs = []
    try:
        proposals = load_queue()
        # Filter for pending proposals only
        available_jobs = [p for p in proposals if p.get('status') == 'pending']
        # Sort by timestamp (most recent first)
        available_jobs.sort(key=lambda x: x.get('timestamp', x.get('created_at', '')), reverse=True)
    except Exception as e:
        logger.error(f"Error loading jobs from queue: {e}")
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upwork Dashboard | Projekt AI</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { margin:0; padding:0; box-sizing:border-box; }
            html, body { font-family:'Inter', -apple-system, BlinkMacSystemFont, sans-serif; line-height:1.6; color:#fff; background:#1a1a1a; overflow-x:hidden; }
            .container { max-width:1400px; margin:0 auto; padding:0 60px; }
            header { position:fixed; top:0; left:0; right:0; background:rgba(26,26,26,0.95); backdrop-filter:blur(20px); z-index:1000; padding:20px 0; border-bottom:1px solid rgba(255,255,255,0.1); }
            nav { display:flex; justify-content:space-between; align-items:center; }
            .logo { font-size:20px; font-weight:500; color:#fff; text-decoration:none; letter-spacing:0.02em; }
            main { margin-top:120px; }
            .jobs-container { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:40px; backdrop-filter:blur(20px); }
            .jobs-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; }
            .job-count { font-size:1rem; color:rgba(255,255,255,0.8); }
            .job-list { display:grid; grid-template-columns:repeat(auto-fit,minmax(400px,1fr)); gap:32px; }
            .job-card { background:#18181b; border:1px solid #23232a; border-radius:16px; box-shadow:0 2px 8px 0 rgba(0,0,0,0.12); padding:32px 28px 24px 28px; transition:box-shadow 0.2s; position:relative; display:flex; flex-direction:column; min-height:320px; }
            .job-card:hover { box-shadow:0 6px 24px 0 rgba(0,0,0,0.22); }
            .job-title { font-size:1.35rem; font-weight:600; margin-bottom:10px; color:#fff; }
            .job-description { color:#d1d5db; margin-bottom:18px; font-size:1rem; min-height:48px; }
            .job-tags { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px; }
            .job-tag { background:#23232a; color:#a3e635; font-size:0.92rem; padding:4px 14px; border-radius:9999px; font-weight:500; letter-spacing:0.01em; }
            .job-meta { display:flex; align-items:center; gap:18px; font-size:0.98rem; color:#a1a1aa; margin-bottom:10px; flex-wrap:wrap; }
            .job-meta .meta-icon { margin-right:6px; font-size:1.1em; vertical-align:middle; }
            .job-meta .meta-label { margin-right:2px; }
            .job-actions { margin-top:auto; display:flex; gap:12px; }
            .view-upwork-btn, .generate-proposal-btn, .reject-btn { 
                border:none; outline:none; font-family:inherit; font-size:1rem; border-radius:9999px; padding:10px 22px; cursor:pointer; transition:background 0.2s, color 0.2s, border 0.2s; 
            }
            .view-upwork-btn { 
                background:#23232a; color:#3b82f6; border:1.5px solid #3b82f6; 
            }
            .view-upwork-btn:hover { 
                background:#3b82f6; color:#fff; border:1.5px solid #fff; 
            }
            .generate-proposal-btn { 
                background:#23232a; color:#fff; border:1.5px solid #393944; 
            }
            .generate-proposal-btn:hover { 
                background:#393944; color:#fff; border:1.5px solid #fff; 
            }
            .reject-btn { 
                background:#23232a; color:#fff; border:1.5px solid #393944; 
            }
            .reject-btn:hover { 
                background:#393944; color:#fff; border:1.5px solid #fff; 
            }
            .job-footer { display:flex; justify-content:space-between; align-items:center; margin-top:18px; font-size:0.95rem; color:#a1a1aa; }
            .job-country { display:flex; align-items:center; gap:6px; }
            .job-country-flag { font-size:1.1em; }
            .job-payment { color:#22d3ee; font-size:1.1em; margin-right:4px; }
            .job-budget { color:#a3e635; font-weight:500; margin-left:8px; }
            .job-score { margin-left:8px; font-weight:500; }
            .job-posted { font-size:0.92rem; color:#71717a; }
            .show-more { color:#3b82f6; cursor:pointer; text-decoration:underline; margin-left:4px; }
            @media (max-width: 700px) {
                .container { padding:0 10px; }
                .job-list { grid-template-columns:1fr; }
            }
        </style>
        <script>
        function toggleDescription(id) {
            var el = document.getElementById('desc-' + id);
            var more = document.getElementById('more-' + id);
            if (el.classList.contains('truncated')) {
                el.classList.remove('truncated');
                more.innerText = 'less';
            } else {
                el.classList.add('truncated');
                more.innerText = 'more';
            }
        }
        </script>
    </head>
    <body>
        <div class="container">
            <header>
                <nav class="container">
                    <a href="/" class="logo">Projekt AI Dashboard</a>
                </nav>
            </header>
            <main style="margin-top:120px;">
            <div class="jobs-container">
                <div class="jobs-header">
                    <h2>Jobs from Chrome Extension</h2>
                    <span class="job-count">{{ available_jobs|length }} jobs</span>
                </div>
                {% if available_jobs %}
                    <div class="job-list">
                        {% for job in available_jobs %}
                            <div class="job-card">
                                <div class="job-title">{{ job.job_title }}</div>
                                <div class="job-tags">
                                    {% for tag in (job.technologies_used or '').split(',') if tag.strip() %}
                                        <span class="job-tag">{{ tag.strip() }}</span>
                                    {% endfor %}
                                </div>
                                <div class="job-meta">
                                    <span class="job-payment meta-icon">&#10003;</span> <span class="meta-label">Payment verified</span>
                                    <span class="job-budget">{{ job.budget or 'Budget not specified' }}</span>
                                    <span class="job-country">
                                        <span class="job-country-flag">&#127482;&#127480;</span> <!-- US flag as example -->
                                        {{ job.client_location or job.country or 'Unknown' }}
                                    </span>
                                    <span class="job-score">Score: {{ job.score or 'N/A' }}</span>
                                    <span class="job-posted">{{ job.created_at }}</span>
                                </div>
                                <div class="job-description" id="desc-{{ job.job_id }}">
                                    {{ job.description[:180] }}{% if job.description|length > 180 %}...<span class="show-more" id="more-{{ job.job_id }}" onclick="toggleDescription('{{ job.job_id }}')">more</span>{% endif %}
                                </div>
                                <div class="job-actions">
                                    <a href="{{ job.url or job.original_job_url or '#' }}" class="view-upwork-btn" target="_blank" rel="noopener noreferrer">View on Upwork</a>
                                    <form action="/generate-from-queue" method="post" style="display: inline;">
                                        <input type="hidden" name="job_id" value="{{ job.job_id }}">
                                        <button type="submit" class="generate-proposal-btn">Generate Proposal</button>
                                    </form>
                                    <form action="/reject-job" method="post" style="display: inline;">
                                        <input type="hidden" name="job_id" value="{{ job.job_id }}">
                                        <button type="submit" class="reject-btn">Reject</button>
                                    </form>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="empty-list">
                        <p>No jobs available from Chrome Extension</p>
                        <p>Make sure your Chrome extension is configured to send jobs to the webhook URL above</p>
                    </div>
                {% endif %}
            </div>
            </main>
            <footer>
                <p>Upwork Proposal Generator</p>
                <p>Powered by Multi-Model AI</p>
            </footer>
        </div>
    </body>
    </html>
    """, available_jobs=available_jobs, port=PORT)

@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate proposal from URL or manual input
    """
    logger.info("Received /generate request")
    # Check if we're coming from manual input form
    if 'job_title' in request.form and 'job_description' in request.form:
        # Process manual input
        logger.info("Processing manual input form data")
        job_url = request.form.get('job_url', '#')
        job_details = {
            "job_title": request.form.get('job_title', ''),
            "description": request.form.get('job_description', ''),
            "budget": request.form.get('budget', 'Not specified'),
            "client_name": request.form.get('client_name', 'Client'),
            "job_url": job_url,
            "url": job_url  # Add both keys for compatibility
        }
    else:
        # Process from URL
        job_url = request.form.get('job_url', '')
        logger.info(f"Processing job from URL: {job_url}")
        
        if not job_url:
            logger.warning("No job URL provided")
            return "Error: No job URL provided", 400
        
        # Extract job details from URL
        job_details = extract_job_details(job_url)
        
        # If extraction failed, show manual input form
        if job_details.get('extraction_failed', False):
            logger.warning(f"Job extraction failed, showing manual input form")
            return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Manual Job Details</title>
                <style>
                    body {
                        font-family: 'Inter', -apple-system, sans-serif;
                        background: #0f172a;
                        color: #e2e8f0;
                        line-height: 1.6;
                        padding: 0;
                        margin: 0;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 40px 20px;
                    }
                    h1 {
                        color: #f8fafc;
                        margin-bottom: 30px;
                        font-weight: 700;
                    }
                    .card {
                        background: #1e293b;
                        border-radius: 8px;
                        padding: 30px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-bottom: 30px;
                    }
                    label {
                        display: block;
                        margin-bottom: 10px;
                        color: #cbd5e1;
                        font-weight: 500;
                    }
                    input[type="text"], textarea {
                        width: 100%;
                        padding: 12px;
                        border: 1px solid #334155;
                        border-radius: 6px;
                        background: #0f172a;
                        color: #f8fafc;
                        font-size: 16px;
                        margin-bottom: 20px;
                        box-sizing: border-box;
                    }
                    textarea {
                        min-height: 200px;
                        resize: vertical;
                    }
                    button {
                        background: #3b82f6;
                        color: white;
                        border: none;
                        padding: 12px 20px;
                        border-radius: 6px;
                        font-size: 16px;
                        font-weight: 500;
                        cursor: pointer;
                        transition: background 0.3s;
                    }
                    button:hover {
                        background: #2563eb;
                    }
                    .alert {
                        background: #7f1d1d;
                        color: #fecaca;
                        padding: 16px;
                        border-radius: 6px;
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Manual Job Details Entry</h1>
                    
                    <div class="alert">
                        <p><strong>Unable to extract job details automatically.</strong></p>
                        <p>Upwork is blocking our automated access. Please enter the job details manually:</p>
                    </div>
                    
                    <div class="card">
                        <form id="manualForm" action="/generate" method="post">
                            <input type="hidden" name="job_url" value="{{ job_url }}">
                            
                            <label for="job_title">Job Title</label>
                            <input type="text" id="job_title" name="job_title" required>
                            
                            <label for="job_description">Job Description</label>
                            <textarea id="job_description" name="job_description" required></textarea>
                            
                            <label for="budget">Budget (if specified)</label>
                            <input type="text" id="budget" name="budget" value="Not specified">
                            
                            <label for="client_name">Client Name (if known)</label>
                            <input type="text" id="client_name" name="client_name" value="Client">
                            
                            <button type="submit">Generate Proposal</button>
                        </form>
                    </div>
                </div>
            </body>
            </html>
            """, job_url=job_url)
    
    # Generate proposal using ONLY Multi-Model AI
    proposal_data = generate_proposal(job_details)
    
    # Check if there was an error
    if proposal_data.get('error', False):
        logger.error(f"Multi-Model AI error: {proposal_data.get('error_message', 'Unknown error')}")
        
        # Return a professional error page
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Proposal Generation Error</title>
            <style>
                body {
                    font-family: 'Inter', -apple-system, sans-serif;
                    background: #0f172a;
                    color: #e2e8f0;
                    line-height: 1.6;
                    padding: 0;
                    margin: 0;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 40px 20px;
                }
                .error-card {
                    background: #1e293b;
                    border: 1px solid #dc2626;
                    border-radius: 8px;
                    padding: 30px;
                    margin-bottom: 30px;
                }
                .error-header {
                    display: flex;
                    align-items: center;
                    margin-bottom: 20px;
                }
                .error-icon {
                    font-size: 2rem;
                    margin-right: 15px;
                }
                .error-title {
                    color: #dc2626;
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin: 0;
                }
                .job-info {
                    background: #0f172a;
                    padding: 20px;
                    border-radius: 6px;
                    margin: 20px 0;
                }
                .error-details {
                    background: #7f1d1d;
                    color: #fecaca;
                    padding: 15px;
                    border-radius: 6px;
                    margin: 15px 0;
                    font-family: monospace;
                    font-size: 0.9rem;
                }
                .actions {
                    margin-top: 30px;
                }
                .btn {
                    background: #3b82f6;
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 6px;
                    font-size: 16px;
                    text-decoration: none;
                    display: inline-block;
                    margin-right: 10px;
                    transition: background 0.3s;
                }
                .btn:hover {
                    background: #2563eb;
                }
                .btn-secondary {
                    background: #6b7280;
                }
                .btn-secondary:hover {
                    background: #4b5563;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error-card">
                    <div class="error-header">
                        <div class="error-icon">&#10060;</div>
                        <h1 class="error-title">Multi-Model AI Unavailable</h1>
                    </div>
                    
                    <p><strong>Unable to generate high-quality proposal</strong></p>
                    <p>Our Multi-Model AI system (GPT-4 + Gemini + Cohere) is currently unavailable. We only provide premium AI-generated proposals to ensure the highest quality.</p>
                    
                    <div class="job-info">
                        <h3>Job Details:</h3>
                        <p><strong>Title:</strong> {{ job_title }}</p>
                        <p><strong>Client:</strong> {{ client_name }}</p>
                        <p><strong>Budget:</strong> {{ budget }}</p>
                    </div>
                    
                    <div class="error-details">
                        <strong>Error:</strong> {{ error_message }}<br>
                        <strong>Details:</strong> {{ error_details }}
                    </div>
                    
                    <div class="actions">
                        <a href="/" class="btn">Back to Dashboard</a>
                        <form action="/generate" method="post" style="display: inline;">
                            <input type="hidden" name="job_url" value="{{ job_url }}">
                            <button type="submit" class="btn btn-secondary">Try Again</button>
                        </form>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """, 
        job_title=proposal_data.get('job_title', 'Unknown Job'),
        client_name=proposal_data.get('client_name', 'Unknown Client'),
        budget=proposal_data.get('budget', 'Unknown Budget'),
        error_message=proposal_data.get('error_message', 'Unknown error'),
        error_details=proposal_data.get('error_details', 'No additional details')
        ), 500
    
    # Format with template (only if successful)
    formatted_proposal = format_proposal_with_template(proposal_data)
    
    # Return formatted proposal
    logger.info(f"Successfully generated and formatted proposal for {job_details['job_title']}")
    return formatted_proposal

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """
    API endpoint for generating proposals
    """
    logger.info("Received /api/generate request")
    data = request.json
    job_url = data.get('job_url', '')
    
    if not job_url:
        logger.warning("API request missing job_url")
        return jsonify({"error": "No job URL provided"}), 400
    
    logger.info(f"API request for job URL: {job_url}")
    
    # Extract job details from URL
    job_details = extract_job_details(job_url)
    
    # Generate proposal
    proposal_data = generate_proposal(job_details)
    
    # Return JSON response
    logger.info(f"Successfully generated proposal via API for {job_details['job_title']}")
    return jsonify(proposal_data)

@app.route('/generate-from-queue', methods=['POST'])
def generate_from_queue():
    """
    Generate proposal from a job in the queue using ONLY Multi-Model AI
    """
    try:
        logger.info(f"Incoming request headers: {request.headers}")  # New log for headers
        if not request.is_json:
            logger.error('Received non-JSON request on /generate-from-queue; Content-Type is not application/json')
            return jsonify({'error': 'Unsupported Media Type: Please send requests with Content-Type: application/json'}), 415
        required_fields = ['job_id', 'job_title', 'description', 'client_name']
        if not all(field in request.json for field in required_fields):
            return jsonify({'error': 'Missing required fields', 'required': required_fields}), 400
        
        job_id = request.json.get('job_id')
        if not job_id:
            logger.warning("No job ID provided for queue generation")
            return "Error: No job ID provided", 400
        
        logger.info(f"Generating proposal for queue job ID: {job_id}")
        
        # Find the job in the queue
        try:
            with open(QUEUE_FILE, 'r') as f:
                proposals = json.load(f)
                
            # Find the job with the matching ID
            job = None
            for p in proposals:
                if p.get('job_id') == job_id:
                    job = p
                    break
                
            if not job:
                logger.warning(f"Job ID {job_id} not found in queue")
                return "Error: Job not found in queue", 404
            
            # Generate the proposal using ONLY Multi-Model AI
            proposal_result = generate_proposal(job)
            logger.info(f"AI proposal_result: {proposal_result}")

            # Handle NoneType or invalid responses
            if not proposal_result or not isinstance(proposal_result, dict):
                logger.error(f"AI server did not return a valid response for job {job_id}. Response: {proposal_result}")
                return render_template_string("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>AI Unavailable - Upwork Proposal Generator</title>
                    <style>
                        {{ error_page_styles }}
                    </style>
                </head>
                <body>
                    <div class="error-container">
                        <div class="error-icon">X</div>
                        <h1 class="error-title">Multi-Model AI Unavailable</h1>
                        <p class="error-subtitle">Unable to generate high-quality proposal</p>
                        <p class="error-description">Our Multi-Model AI system (GPT-4 + Gemini + Cohere) is currently unavailable or returned an invalid response. Please try again later.</p>
                        <div class="job-details">
                            <h3>Job Details:</h3>
                            <div class="detail-item"><strong>Title:</strong> {{ job_title }}</div>
                            <div class="detail-item"><strong>Client:</strong> {{ client_name }}</div>
                            <div class="detail-item"><strong>Budget:</strong> {{ budget }}</div>
                            <div class="detail-item"><strong>Job ID:</strong> {{ job_id }}</div>
                        </div>
                        <div class="error-details">
                            <h4>Error Details:</h4>
                            <p>AI server did not return a valid response.</p>
                        </div>
                        <div class="action-buttons">
                            <a href="/" class="back-button">Back to Dashboard</a>
                            <button onclick="window.location.reload()" class="retry-button">Try Again</button>
                        </div>
                    </div>
                </body>
                </html>
                """, 
                error_page_styles=get_error_page_styles(),
                job_title=job.get('job_title', 'Unknown'),
                client_name=job.get('client_name', 'Unknown'),
                budget=job.get('budget', 'Not specified'),
                job_id=job.get('job_id', 'Unknown')
                ), 500

            # Handle different types of errors
            if proposal_result.get("error"):
                error_type = proposal_result.get("error_type", "unknown")
                
                if error_type == "job_rejected":
                    # Job was rejected by AI - show rejection page
                    logger.error(f"Multi-Model AI rejected queue job {job_id}: {proposal_result.get('rejection_reason', 'No reason provided')}")
                    
                    return render_template_string("""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Job Rejected - Upwork Proposal Generator</title>
                        <style>
                            {{ error_page_styles }}
                        </style>
                    </head>
                    <body>
                        <div class="error-container">
                            <div class="error-icon">X</div>
                            <h1 class="error-title">Job Rejected by AI</h1>
                            <p class="error-subtitle">This job does not meet our quality criteria</p>
                            <p class="error-description">{{ error_message }}</p>
                            
                            <div class="job-details">
                                <h3>Job Details:</h3>
                                <div class="detail-item"><strong>Title:</strong> {{ job_title }}</div>
                                <div class="detail-item"><strong>Client:</strong> {{ client_name }}</div>
                                <div class="detail-item"><strong>Budget:</strong> {{ budget }}</div>
                                <div class="detail-item"><strong>Job ID:</strong> {{ job_id }}</div>
                            </div>
                            
                            <div class="rejection-details">
                                <h4>Rejection Reason:</h4>
                                <p>{{ rejection_reason }}</p>
                            </div>
                            
                            <div class="action-buttons">
                                <a href="/" class="back-button">Back to Dashboard</a>
                                <form action="/reject-job" method="post" style="display: inline;">
                                    <input type="hidden" name="job_id" value="{{ job_id }}">
                                    <button type="submit" class="reject-button">Remove Job</button>
                                </form>
                            </div>
                        </div>
                    </body>
                    </html>
                    """, 
                    error_page_styles=get_error_page_styles(),
                    error_message=proposal_result.get("error_message", "Job was rejected"),
                    job_title=proposal_result.get("job_title", "Unknown"),
                    client_name=proposal_result.get("client_name", "Unknown"),
                    budget=proposal_result.get("budget", "Not specified"),
                    job_id=proposal_result.get("job_id", "Unknown"),
                    rejection_reason=proposal_result.get("rejection_reason", "Did not meet criteria")
                    ), 422  # 422 Unprocessable Entity
                    
                else:
                    # AI server error or unavailable - show unavailable page
                    logger.error(f"Multi-Model AI error for queue job {job_id}: {proposal_result.get('error_message', 'Unknown error')}")
                    
                    return render_template_string("""
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>AI Unavailable - Upwork Proposal Generator</title>
                        <style>
                            {{ error_page_styles }}
                        </style>
                    </head>
                    <body>
                        <div class="error-container">
                            <div class="error-icon">X</div>
                            <h1 class="error-title">Multi-Model AI Unavailable</h1>
                            <p class="error-subtitle">Unable to generate high-quality proposal</p>
                            <p class="error-description">Our Multi-Model AI system (GPT-4 + Gemini + Cohere) is currently unavailable or returned an invalid response. Please try again later.</p>
                            <div class="job-details">
                                <h3>Job Details:</h3>
                                <div class="detail-item"><strong>Title:</strong> {{ job_title }}</div>
                                <div class="detail-item"><strong>Client:</strong> {{ client_name }}</div>
                                <div class="detail-item"><strong>Budget:</strong> {{ budget }}</div>
                                <div class="detail-item"><strong>Job ID:</strong> {{ job_id }}</div>
                            </div>
                            <div class="error-details">
                                <h4>Error Details:</h4>
                                <p>AI server did not return a valid response.</p>
                            </div>
                            <div class="action-buttons">
                                <a href="/" class="back-button">Back to Dashboard</a>
                                <button onclick="window.location.reload()" class="retry-button">Try Again</button>
                            </div>
                        </div>
                    </body>
                    </html>
                    """, 
                    error_page_styles=get_error_page_styles(),
                    job_title=job.get('job_title', 'Unknown'),
                    client_name=job.get('client_name', 'Unknown'),
                    budget=job.get('budget', 'Not specified'),
                    job_id=job.get('job_id', 'Unknown')
                    ), 500
            
            # Ensure the original job data is preserved in the successful proposal
            proposal_result['job_title'] = job.get('job_title', proposal_result.get('job_title', 'Unknown Job'))
            proposal_result['client_name'] = job.get('client_name', proposal_result.get('client_name', 'Client'))
            proposal_result['budget'] = job.get('budget', proposal_result.get('budget', 'Not specified'))
            proposal_result['description'] = job.get('description', proposal_result.get('description', ''))
            proposal_result['original_job_url'] = job.get('url', job.get('original_job_url', '#'))
            
            logger.info(f"Proposal data prepared with title: {proposal_result.get('job_title')}")
            
            # Format the proposal with template
            formatted_proposal = format_proposal_with_template(proposal_result)
            
            # Return formatted proposal
            logger.info(f"Successfully generated proposal from queue for job ID: {job_id}")
            return formatted_proposal
            
        except Exception as e:
            logger.error(f"Error processing queue job: {e}")
            return f"Error processing job from queue: {str(e)}", 500
    except Exception as e:
        logger.error(f'Error in /generate-from-queue: {str(e)}')
        return jsonify({'error': 'Internal server error processing request'}), 500

@app.route('/reject-job', methods=['POST'])
def reject_job():
    """
    Reject a job from the queue
    """
    job_id = request.form.get('job_id')
    
    if not job_id:
        return "No job ID provided", 400
    
    try:
        # Load the queue
        proposals = load_queue()
        
        # Find and update the job status
        job_found = False
        for proposal in proposals:
            if proposal.get('job_id') == job_id:
                proposal['status'] = 'rejected'
                job_found = True
                logger.info(f"Rejected job: {job_id}")
                break
        
        if job_found:
            # Save the updated queue
            save_queue(proposals)
            return redirect('/')
        else:
            return f"Job {job_id} not found", 404
            
    except Exception as e:
        logger.error(f"Error rejecting job: {e}")
        return f"Error rejecting job: {str(e)}", 500

@app.route('/webhook/rss-jobs', methods=['POST'])
def webhook_rss_jobs():
    """
    Webhook endpoint to receive jobs from Chrome extension
    """
    try:
        # Parse JSON payload (single object or list)
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON payload"}), 400
        jobs = data if isinstance(data, list) else [data]
        logger.info(f"Received {len(jobs)} job(s) via webhook")
        # Load existing queue
        proposals = load_queue()
        added = 0
        for job_data in jobs:
            logger.info(f"Full incoming job_data: {json.dumps(job_data, indent=2)}")
            title = job_data.get('title', 'Unknown')
            logger.info(f"Processing job via webhook: {title}")
            job_id = job_data.get('job_id', f"job_{int(time.time() * 1000)}")
            # NEW: Try to get location/country from job_data
            client_location = job_data.get('client_location') or job_data.get('location') or job_data.get('country') or ''
            job_entry = {
                "job_id": job_id,
                "job_title": job_data.get('title', 'Unknown Job'),
                "client_name": job_data.get('client_name', 'Client'),
                "client_location": client_location,  # NEW FIELD
                "budget": job_data.get('budget', 'N/A'),
                "description": job_data.get('description', ''),
                "url": job_data.get('url', ''),
                "original_job_url": job_data.get('url', ''),
                "status": "pending",
                "created_at": datetime.datetime.now().isoformat(),
                "timestamp": datetime.datetime.now().isoformat(),
                "source": "chrome_extension"
            }
            # Avoid duplicates
            if not any(p.get('job_id') == job_id for p in proposals):
                proposals.append(job_entry)
                added += 1
        
        # Save queue and respond
        if save_queue(proposals):
            logger.info(f"Successfully added {added} job(s) to queue")
            return jsonify({"success": True, "message": f"{added} job(s) added to queue"}), 200
        else:
            return jsonify({"success": False, "error": "Failed to save job(s)"}), 500
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

# Helper functions
def get_error_page_styles():
    """Return CSS styles for error pages"""
    return """
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            line-height: 1.6;
            padding: 0;
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .error-container {
            max-width: 600px;
            width: 90%;
            background: #1e293b;
            border: 1px solid #dc2626;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        .error-icon {
            font-size: 4rem;
            margin-bottom: 20px;
            display: block;
        }
        .error-title {
            color: #dc2626;
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 10px 0;
        }
        .error-subtitle {
            color: #cbd5e1;
            font-size: 1.125rem;
            margin: 0 0 20px 0;
        }
        .error-description {
            color: #94a3b8;
            margin-bottom: 30px;
            font-size: 1rem;
        }
        .job-details {
            background: #0f172a;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            text-align: left;
        }
        .job-details h3 {
            color: #e2e8f0;
            margin: 0 0 15px 0;
            font-size: 1.125rem;
        }
        .job-details h4 {
            color: #e2e8f0;
            margin: 15px 0 10px 0;
            font-size: 1rem;
        }
        .detail-item {
            margin: 8px 0;
            color: #cbd5e1;
        }
        .detail-item strong {
            color: #e2e8f0;
        }
        .rejection-details {
            background: #7f1d1d;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            text-align: left;
        }
        .rejection-details h4 {
            color: #fecaca;
            margin: 0 0 10px 0;
        }
        .rejection-details p {
            color: #fecaca;
            margin: 0;
            font-style: italic;
        }
        .error-details {
            background: #0f172a;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            text-align: left;
        }
        .error-details h4 {
            color: #e2e8f0;
            margin: 0 0 10px 0;
        }
        .error-details p {
            color: #cbd5e1;
            margin: 0;
            font-family: monospace;
            font-size: 0.9rem;
        }
        .action-buttons {
            margin-top: 30px;
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .back-button, .retry-button, .reject-button {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 16px;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s;
            cursor: pointer;
        }
        .back-button:hover, .retry-button:hover {
            background: #2563eb;
        }
        .reject-button {
            background: #dc2626;
        }
        .reject-button:hover {
            background: #b91c1c;
        }
        @media (max-width: 640px) {
            .error-container {
                padding: 30px 20px;
            }
            .error-title {
                font-size: 1.5rem;
            }
            .action-buttons {
                flex-direction: column;
                align-items: center;
            }
            .back-button, .retry-button, .reject-button {
                width: 100%;
                max-width: 200px;
            }
        }
    """

if __name__ == '__main__':
    print(f"\n🚀 Starting Simple Upwork Proposal Generator on port {PORT}")
    print(f"📊 Using Multi-Model AI Server at {MULTIMODEL_SERVER}")
    print(f"🌐 Open your browser to http://localhost:{PORT}")
    print(f"🔗 Chrome Extension Webhook: http://192.168.1.107:{PORT}/webhook/rss-jobs")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=PORT, debug=True) 