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
PORT = 5001  # STANDARDIZED: Category E (External APIs)
PROPOSALS_DIR = "/srv/apps/client-proposals/public/"
QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
GEMINI_API_KEY = "AIzaSyDd5ZmjEGExtFuiEwhIk15glVGVXjsIjNg"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

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
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        """Handle incoming webhook from Upwork scraper"""
        if self.path == '/webhook/rss-jobs':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                jobs = json.loads(post_data)
                
                # Process each job
                for job in jobs:
                    proposal_data = self.process_job(job)
                    self.save_to_queue(proposal_data)
                    self.save_proposal_html(proposal_data)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "processed": len(jobs)}).encode())
                
            except Exception as e:
                self.send_error(500, f"Error processing jobs: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found")
    
    def process_job(self, job):
        """Process a single job and generate proposal"""
        
        # Extract job details
        job_title = job.get('title', 'Untitled Job')
        job_description = job.get('description', '')
        budget = job.get('budget', 'Not specified')
        client_name = self.extract_client_name(job)
        
        # Analyze job with basic NLP
        job_analysis = self.analyze_job(job_title, job_description)
        
        # Generate proposal with Gemini
        proposal_message = self.generate_proposal_with_gemini(
            job_title, job_description, budget, job_analysis
        )
        
        # Create proposal data
        proposal_data = {
            "job_id": job.get('guid', f"job_{int(time.time())}"),
            "job_title": job_title,
            "client_name": client_name,
            "budget": budget,
            "description": job_description[:500] + "..." if len(job_description) > 500 else job_description,
            "analysis": job_analysis,
            "message": proposal_message,
            "score": job_analysis.get('score', 75),
            "created_at": datetime.now().isoformat(),
            "proposal_url": f"https://projekt-ai.net/proposals/{self.generate_filename(job_title)}",
            "original_job_url": job.get('link', ''),
            "status": "pending"
        }
        
        return proposal_data
    
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
        """Basic job analysis"""
        
        text = f"{title} {description}".lower()
        
        # Detect tools mentioned
        tools = []
        tool_keywords = ['zapier', 'make.com', 'integromat', 'n8n', 'api', 'webhook']
        for tool in tool_keywords:
            if tool in text:
                tools.append(tool.title())
        
        # Detect pain points
        pain_points = []
        pain_keywords = {
            'manual': 'manual processes',
            'time-consuming': 'time-consuming tasks',
            'repetitive': 'repetitive work',
            'integrate': 'integration challenges',
            'automate': 'automation needs'
        }
        
        for keyword, pain in pain_keywords.items():
            if keyword in text:
                pain_points.append(pain)
        
        # Detect industry
        industry = 'general business'
        industries = {
            'restaurant': 'restaurant/hospitality',
            'ecommerce': 'e-commerce',
            'saas': 'SaaS',
            'real estate': 'real estate',
            'healthcare': 'healthcare'
        }
        
        for keyword, ind in industries.items():
            if keyword in text:
                industry = ind
                break
        
        # Calculate score
        score = 70  # Base score
        if tools:
            score += 10
        if len(pain_points) > 1:
            score += 10
        if 'urgent' in text or 'asap' in text:
            score += 10
        
        return {
            'tools': tools or ['Zapier', 'Make.com'],
            'pain_points': pain_points or ['manual processes'],
            'industry': industry,
            'score': min(score, 100)
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
        
        queue_file = os.path.join(os.path.dirname(__file__), 'proposal-queue.json')
        
        try:
            # Load existing queue
            if os.path.exists(queue_file):
                with open(queue_file, 'r') as f:
                    queue = json.load(f)
            else:
                queue = []
            
            # Add new proposal
            queue.append(proposal_data)
            
            # Keep only last 100 proposals
            queue = queue[-100:]
            
            # Save updated queue
            with open(queue_file, 'w') as f:
                json.dump(queue, f, indent=2)
            
            # Sync to web directory for dashboard
            web_queue = "/srv/apps/client-proposals/public/proposal-queue.json"
            os.makedirs(os.path.dirname(web_queue), exist_ok=True)
            with open(web_queue, 'w') as f:
                json.dump(queue, f, indent=2)
                
        except Exception as e:
            print(f"Error saving to queue: {e}")
    
    def save_proposal_html(self, proposal_data):
        """Save proposal as HTML file"""
        
        filename = self.generate_filename(proposal_data['job_title'])
        filepath = os.path.join(PROPOSALS_DIR, filename)
        
        # Create HTML content
        html_content = self.generate_html_template(proposal_data)
        
        try:
            os.makedirs(PROPOSALS_DIR, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(html_content)
            print(f"✅ Saved proposal: {filename}")
        except Exception as e:
            print(f"Error saving HTML: {e}")
    
    def generate_filename(self, job_title):
        """Generate safe filename from job title"""
        
        # Clean title
        safe_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_'))
        safe_title = safe_title.replace(' ', '-')[:50]
        
        # Add timestamp
        timestamp = int(time.time() * 1000)
        
        return f"proposal-{safe_title}-{timestamp}.html"
    
    def generate_html_template(self, data):
        """Generate HTML template for proposal"""
        
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
    
    with socketserver.TCPServer(("", PORT), UpworkProposalServer) as httpd:
        print(f"🚀 Upwork Proposal Server with Gemini running on port {PORT}")
        print(f"📡 Webhook URL: http://192.168.1.107:{PORT}/webhook/rss-jobs")
        print(f"📝 Proposals saved to: {PROPOSALS_DIR}")
        print(f"📋 Review queue: {QUEUE_FILE}")
        print(f"✨ Using Gemini AI for enhanced proposals")
        print(f"✅ Ready to receive jobs from Upwork scraper!")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server() 