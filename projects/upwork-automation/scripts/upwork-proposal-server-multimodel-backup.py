#!/usr/bin/env python3
"""
Upwork Proposal Server with Gemini Integration
Uses Gemini API for enhanced proposal generation without requiring google-generativeai library
"""

import http.server
import socketserver
import json
import os
import requests
from datetime import datetime
from urllib.parse import parse_qs
import threading
import time

# Configuration
PORT = 5056  # Reverted to match logs
PROPOSALS_DIR = "/srv/apps/client-proposals/public/"
QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
GEMINI_API_KEY = "AIzaSyDd5ZmjEGExtFuiEwhIk15glVGVXjsIjNg"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

class ReusableUpworkServer(socketserver.TCPServer):
    """Custom TCPServer that allows address reuse to prevent 'Address already in use' errors"""
    allow_reuse_address = True

class UpworkProposalServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests for dashboard"""
        if self.path == '/api/proposals':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Load proposals from queue file
            try:
                with open(QUEUE_FILE, 'r') as f:
                    proposals = json.load(f)
                    # Sort by timestamp (most recent first)
                    if isinstance(proposals, list):
                        proposals.sort(key=lambda x: x.get('timestamp', x.get('created_at', '')), reverse=True)
                    self.wfile.write(json.dumps(proposals).encode())
            except:
                self.wfile.write(json.dumps([]).encode())
        elif self.path == '/data/proposals.json':
            # Dashboard endpoint - serve proposals in expected format
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open(QUEUE_FILE, 'r') as f:
                    proposals = json.load(f)
                    # Sort by timestamp (most recent first)
                    if isinstance(proposals, list):
                        proposals.sort(key=lambda x: x.get('timestamp', x.get('created_at', '')), reverse=True)
                    
                    # Format for dashboard
                    dashboard_data = {
                        "proposals": proposals,
                        "generated_at": datetime.now().isoformat(),
                        "total_count": len(proposals)
                    }
                    self.wfile.write(json.dumps(dashboard_data).encode())
            except Exception as e:
                print(f"Error loading proposals: {e}")
                self.wfile.write(json.dumps({
                    "proposals": [],
                    "generated_at": datetime.now().isoformat(),
                    "total_count": 0,
                    "error": str(e)
                }).encode())
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        """Handle incoming webhook from Upwork scraper"""
        if self.path == '/webhook/rss-jobs':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                jobs = json.loads(post_data)
                if not isinstance(jobs, list):
                    self.send_error(400, 'Expected a list of jobs')
                    return
                processed_count = 0
                for job in jobs:
                    if isinstance(job, dict):
                        proposal_data = self.process_job(job)
                        if proposal_data:
                            self.save_to_queue(proposal_data)
                            self.save_proposal_html(proposal_data)
                            processed_count += 1
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'processed': processed_count}).encode())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Endpoint not found")
    
    def process_job(self, job):
        """Process a single job and generate proposal"""
        
        try:
            if not isinstance(job, dict):
                return None
            job_title = job.get('title', 'Untitled Job')
            job_description = job.get('description', '')
            budget = job.get('budget', 'Not specified')
            client_name = self.extract_client_name(job)
            timestamp = int(time.time() * 1000)
            job_analysis = self.analyze_job(job_title, job_description)
            if job_analysis.get('rejected', False):
                return None
            proposal_message = self.generate_proposal_with_gemini(job_title, job_description, budget, job_analysis)
            filename = self.generate_filename_with_timestamp(job_title, timestamp)
            proposal_data = {
                'job_id': job.get('guid', f'job_{timestamp}'),
                'job_title': job_title,
                'client_name': client_name,
                'budget': budget,
                'description': job_description[:500] + '...' if len(job_description) > 500 else job_description,
                'analysis': job_analysis,
                'message': proposal_message,
                'score': job_analysis.get('score', 75),
                'created_at': datetime.now().isoformat(),
                'proposal_url': f'https://proposals.projekt-ai.net/{filename}',
                'original_job_url': job.get('link', ''),
                'status': 'pending',
                'filename': filename,
                'automation_terms_found': job_analysis.get('automation_terms_found', 0),
                'specialties': job_analysis.get('specialties', [])
            }
            return proposal_data
        except Exception as e:
            print(f'Error processing job: {e}')
            return None
    
    def generate_proposal_with_gemini(self, job_title, job_description, budget, analysis):
        """Generate proposal using Gemini API via HTTP request"""
        
        prompt = f"""You are Timothy Poulton, a 20-year automation specialist and solo freelancer. Your goal is to write a short, highly believable, and personable Upwork proposal that feels like a real, thoughtful response—not a template or marketing pitch.

Job Title: {job_title}
Budget: {budget}
Description: {job_description[:500]}

Key Pain Points Detected: {', '.join(analysis.get('pain_points', ['manual processes']))}

Write a proposal (100-150 words) that:
1. Opens with a personal reference to the client's specific pain point or project detail (quote or paraphrase from their description).
2. Shares a brief, real anecdote or insight from your experience (no generic numbers or claims, no made-up stats).
3. Outlines a 2-3 step approach tailored to their situation (use their language, not generic automation talk).
4. Closes with a natural, friendly invitation to connect (no hard sell, no 'perfect fit' language).

Use "I" statements, sound like a real person, and make it clear you read their job post. Avoid anything that sounds like a template or sales pitch. Do not use generic claims like 'Having automated 200+ businesses' or 'Last month, I helped a similar client...'.

Return only the proposal text, nothing else."""
        
        try:
            # Make API request to Gemini
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            response = requests.post(GEMINI_API_URL, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                # Extract the generated text
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                return generated_text.strip()
            else:
                print(f"Gemini API error: {response.status_code}")
                return self.generate_fallback_proposal(job_title, analysis)
                
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self.generate_fallback_proposal(job_title, analysis)
    
    def generate_fallback_proposal(self, job_title, analysis):
        """Fallback proposal generation if Gemini fails"""
        
        pain_point = analysis.get('pain_points', ['manual processes'])[0]
        
        return f"""I noticed you're struggling with {pain_point} in your {analysis.get('industry', 'business')}.

Having automated 200+ similar businesses, I can help you save 15+ hours weekly through smart integrations.

My approach:
1. Map your current workflow and identify bottlenecks
2. Build custom automations using {', '.join(analysis.get('tools', ['Zapier', 'Make.com']))}
3. Train your team and provide documentation

Last month, I helped a similar client reduce manual work by 70% while improving accuracy.

I'd love to discuss your specific needs. When would be a good time for a quick call?

Best,
Timothy"""
    
    def analyze_job(self, title, description):
        """Enhanced job analysis using scoring-config.json rules"""
        
        # Load scoring configuration
        scoring_config_path = os.path.join(os.path.dirname(__file__), 'scoring-config.json')
        try:
            with open(scoring_config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading scoring config: {e}")
            return {'tools': [], 'pain_points': [], 'industry': 'unknown', 'score': 0, 'rejected': True}
        
        text = f"{title} {description}".lower()
        score = 70  # Base score
        
        # Check for immediate disqualifiers first
        immediate_disqualifiers = config['scoring_rules']['negative_keywords']['immediate_disqualifiers']['terms']
        development_disqualifiers = config['scoring_rules']['negative_keywords']['development_disqualifiers']['terms']
        
        for term in immediate_disqualifiers + development_disqualifiers:
            if term.lower() in text:
                print(f"❌ REJECTED: Contains disqualifying term '{term}'")
                return {
                    'tools': [],
                    'pain_points': [f"Disqualified: {term}"],
                    'industry': 'rejected',
                    'score': 0,
                    'rejected': True,
                    'reason': f"Contains disqualifying term: {term}"
                }
        
        # Check automation requirement (minimum 2 automation terms required)
        automation_terms = config['filtering']['required_automation_terms']['terms']
        automation_count = sum(1 for term in automation_terms if term.lower() in text)
        min_required = config['filtering']['required_automation_terms']['minimum_required']
        
        if automation_count < min_required:
            print(f"❌ REJECTED: Only {automation_count} automation terms found, {min_required} required")
            return {
                'tools': [],
                'pain_points': ['Insufficient automation terms'],
                'industry': 'rejected',
                'score': 0,
                'rejected': True,
                'reason': f"Only {automation_count}/{min_required} automation terms found"
            }
        
        # Apply positive scoring
        keywords = config['scoring_rules']['keywords']
        
        # AI Automation keywords
        for term in keywords['ai_automation']['terms']:
            if term.lower() in text:
                score += keywords['ai_automation']['points']
                break
        
        # Primary tools
        tools_found = []
        for term in keywords['primary_tools']['terms']:
            if term.lower() in text:
                score += keywords['primary_tools']['points']
                tools_found.append(term.title())
                break
        
        # Timothy's specialties (your specific expertise)
        specialties_found = []
        for term in keywords['timothy_specialties']['terms']:
            if term.lower() in text:
                score += keywords['timothy_specialties']['points']
                specialties_found.append(term)
                break
        
        # Automation type
        for term in keywords['automation_type']['terms']:
            if term.lower() in text:
                score += keywords['automation_type']['points']
                break
        
        # No-code platforms
        for term in keywords['no_code_platforms']['terms']:
            if term.lower() in text:
                score += keywords['no_code_platforms']['points']
                break
        
        # Integration focus
        for term in keywords['integration_focus']['terms']:
            if term.lower() in text:
                score += keywords['integration_focus']['points']
                break
        
        # Business processes
        for term in keywords['business_processes']['terms']:
            if term.lower() in text:
                score += keywords['business_processes']['points']
                break
        
        # Hospitality bonus
        for term in keywords['hospitality_bonus']['terms']:
            if term.lower() in text:
                score += keywords['hospitality_bonus']['points']
                break
        
        # Apply negative scoring
        negative_keywords = config['scoring_rules']['negative_keywords']
        
        # Avoid tech stack
        for term in negative_keywords['avoid_tech_stack']['terms']:
            if term.lower() in text:
                score += negative_keywords['avoid_tech_stack']['points']  # This is negative
                break
        
        # Avoid work type  
        for term in negative_keywords['avoid_work_type']['terms']:
            if term.lower() in text:
                score += negative_keywords['avoid_work_type']['points']  # This is negative
                break
        
        # Avoid industries
        for term in negative_keywords['avoid_industries']['terms']:
            if term.lower() in text:
                score += negative_keywords['avoid_industries']['points']  # This is negative
                break
        
        # Reduce score
        for term in negative_keywords['reduce_score']['terms']:
            if term.lower() in text:
                score += negative_keywords['reduce_score']['points']  # This is negative
                break
        
        # Detect industry
        industry = 'general business'
        if any(term in text for term in ['restaurant', 'hospitality', 'venue', 'club', 'bar']):
            industry = 'hospitality'
        elif any(term in text for term in ['ecommerce', 'e-commerce', 'online store']):
            industry = 'e-commerce'
        elif any(term in text for term in ['saas', 'software as a service']):
            industry = 'SaaS'
        elif any(term in text for term in ['real estate', 'property']):
            industry = 'real estate'
        
        # Detect pain points
        pain_points = []
        pain_keywords = {
            'manual': 'manual processes',
            'time-consuming': 'time-consuming tasks', 
            'repetitive': 'repetitive work',
            'integrate': 'integration challenges',
            'automate': 'automation needs',
            'inefficient': 'inefficient workflows',
            'bottleneck': 'process bottlenecks'
        }
        
        for keyword, pain in pain_keywords.items():
            if keyword in text:
                pain_points.append(pain)
        
        # Ensure minimum score requirements
        min_automation_score = config['filtering'].get('min_automation_score', 40)
        if score < min_automation_score:
            print(f"❌ REJECTED: Score {score} below minimum {min_automation_score}")
            return {
                'tools': tools_found,
                'pain_points': pain_points or ['Below minimum score'],
                'industry': industry,
                'score': score,
                'rejected': True,
                'reason': f"Score {score} below minimum {min_automation_score}"
            }
        
        print(f"✅ ACCEPTED: Score {score} - {title[:50]}...")
        
        return {
            'tools': tools_found or ['Automation Tools'],
            'pain_points': pain_points or ['workflow optimization'],
            'industry': industry,
            'score': min(score, 100),
            'rejected': False,
            'specialties': specialties_found,
            'automation_terms_found': automation_count
        }
    
    def extract_client_name(self, job):
        """Extract client name from job data"""
        
        # Try different fields
        client = job.get('client', {})
        if isinstance(client, dict):
            return client.get('name', 'Client')
        elif isinstance(client, str):
            return client
        
        # Fallback
        return job.get('client_name', 'Potential Client')
    
    def save_to_queue(self, proposal_data):
        """Save proposal to review queue"""
        
        try:
            with open(QUEUE_FILE, 'r+') as f:
                proposals = json.load(f)
                if not isinstance(proposals, list):
                    proposals = []
                proposals.append(proposal_data)
                f.seek(0)
                json.dump(proposals, f, indent=2)
        except Exception as e:
            print(f'Error saving to queue: {e}')
    
    def save_proposal_html(self, proposal_data):
        """Save proposal as HTML file"""
        
        try:
            html_content = self.generate_html_template(proposal_data)
            filename = proposal_data['filename']
            with open(os.path.join(PROPOSALS_DIR, filename), 'w') as f:
                f.write(html_content)
        except Exception as e:
            print(f'Error saving proposal HTML: {e}')
    
    def generate_filename(self, job_title):
        """Generate safe filename from job title"""
        
        # Clean title
        safe_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_'))
        safe_title = safe_title.replace(' ', '-')[:50]
        
        # Add timestamp
        timestamp = int(time.time() * 1000)
        
        return f"proposal-{safe_title}-{timestamp}.html"
    
    def generate_filename_with_timestamp(self, job_title, timestamp):
        """Generate safe filename from job title and timestamp"""
        
        # Clean title
        safe_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_'))
        safe_title = safe_title.replace(' ', '-')[:50]
        
        return f"proposal-{safe_title}-{timestamp}.html"
    
    def generate_html_template(self, data):
        """Generate professional dark theme proposal using template"""
        
        # Load the professional dark theme template
        template_path = "/root/homelab-docs/projekt-ai-website/templates/dark-proposal-template.html"
        
        try:
            with open(template_path, 'r') as f:
                template = f.read()
        except Exception as e:
            print(f"Error loading template: {e}")
            return self.generate_fallback_html(data)
        
        # Extract analysis data
        analysis = data.get('analysis', {})
        tools = analysis.get('tools', ['Automation Tools'])
        pain_points = analysis.get('pain_points', ['workflow optimization'])
        industry = analysis.get('industry', 'business')
        
        # Generate project title and subtitle
        project_title = f"Smart {industry.title()} Automation"
        project_subtitle = f"Transform your {pain_points[0]} with intelligent automation workflows"
        
        # Generate workflow steps based on analysis
        workflow_steps = self.generate_workflow_steps(analysis, data['job_title'])
        
        # Generate process steps
        process_steps = self.generate_process_steps(analysis)
        
        # Extract budget information
        budget = data.get('budget', 'Contact for pricing')
        price_range = self.extract_price_range(budget)
        delivery_weeks = self.estimate_delivery_time(analysis)
        
        # Replace template variables
        replacements = {
            '[CLIENT_NAME]': data.get('client_name', 'Valued Client'),
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
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, str(value))
        
        return template
    
    def generate_workflow_steps(self, analysis, job_title):
        """Generate workflow steps based on job analysis"""
        
        industry = analysis.get('industry', 'business')
        tools = analysis.get('tools', ['Automation Platform'])
        
        base_steps = [
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
        
        return base_steps
    
    def generate_process_steps(self, analysis):
        """Generate technical process steps"""
        
        industry = analysis.get('industry', 'business')
        tools = analysis.get('tools', ['Automation Platform'])
        
        return [
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
    
    def extract_price_range(self, budget_text):
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
    
    def estimate_delivery_time(self, analysis):
        """Estimate delivery time based on complexity"""
        
        score = analysis.get('score', 70)
        tools = analysis.get('tools', [])
        
        if score > 85 and len(tools) > 2:
            return "2-3 weeks"
        elif score > 70:
            return "3-4 weeks"
        else:
            return "4-6 weeks"
    
    def generate_fallback_html(self, data):
        """Fallback HTML if template loading fails"""
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['job_title']} - Proposal</title>
    <style>
        body {{ font-family: 'Inter', -apple-system, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1a1a1a; color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .score {{ background: #4CAF50; color: white; padding: 5px 15px; border-radius: 20px; display: inline-block; }}
        .section {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .proposal {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ margin: 0 0 10px 0; }}
        .meta {{ opacity: 0.8; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{data['job_title']}</h1>
        <div class="meta">
            Client: {data['client_name']} | Budget: {data['budget']} | 
            <span class="score">Score: {data['score']}</span>
        </div>
    </div>
    
    <div class="section">
        <h2>Job Description</h2>
        <p>{data['description']}</p>
    </div>
    
    <div class="section">
        <h2>Analysis</h2>
        <p><strong>Industry:</strong> {data['analysis']['industry']}</p>
        <p><strong>Pain Points:</strong> {', '.join(data['analysis']['pain_points'])}</p>
        <p><strong>Tools Mentioned:</strong> {', '.join(data['analysis']['tools'])}</p>
    </div>
    
    <div class="proposal">
        <h2>Your Proposal</h2>
        <div style="white-space: pre-wrap;">{data['message']}</div>
    </div>
    
    <div style="text-align: center; margin-top: 30px; opacity: 0.6;">
        Generated by Projekt AI with Gemini | {data['created_at']}
    </div>
</body>
</html>"""

def run_server():
    """Run the proposal server"""
    
    with ReusableUpworkServer(("", PORT), UpworkProposalServer) as httpd:
        print(f"🚀 Upwork Proposal Server with Gemini running on port {PORT}")
        print(f"📡 Webhook URL: http://192.168.1.107:{PORT}/webhook/rss-jobs")
        print(f"📝 Proposals saved to: {PROPOSALS_DIR}")
        print(f"📋 Review queue: {QUEUE_FILE}")
        print(f"✨ Using Gemini AI for enhanced proposals")
        print(f"✅ Ready to receive jobs from Upwork scraper!")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server() 