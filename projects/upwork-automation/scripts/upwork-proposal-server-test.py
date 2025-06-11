#!/usr/bin/env python3
"""
Upwork Proposal Server with Multi-Model AI - TEST VERSION
Uses GPT-4 + Gemini + Cohere for enhanced proposal generation
TEMPORARY PORT 5002 FOR TESTING
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

# Configuration - PRODUCTION PORT
PORT = 5001  # PRODUCTION: Multi-model AI system on standard port
PROPOSALS_DIR = "/srv/apps/client-proposals/public/"
QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
GEMINI_API_KEY = "AIzaSyDd5ZmjEGExtFuiEwhIk15glVGVXjsIjNg"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Multi-Model AI Configuration
try:
    import openai
    OPENAI_AVAILABLE = True
    openai.api_key = os.environ.get('OPENAI_API_KEY', 'sk-your-key-here')
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI not available - using Gemini fallback")

try:
    import cohere
    COHERE_AVAILABLE = True
    co = cohere.Client(os.environ.get('COHERE_API_KEY', 'your-key-here'))
except ImportError:
    COHERE_AVAILABLE = False
    print("⚠️ Cohere not available - using Gemini fallback")

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
        elif self.path == '/status':
            # Status endpoint for testing
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status = {
                "server": "multi-model-test",
                "port": PORT,
                "ai_models": {
                    "openai": OPENAI_AVAILABLE,
                    "gemini": True,
                    "cohere": COHERE_AVAILABLE
                },
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        """Handle incoming webhook from Upwork scraper"""
        if self.path == '/webhook/rss-jobs':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                jobs = json.loads(post_data)
                
                # Process each job with multi-model AI
                processed_count = 0
                for job in jobs:
                    proposal_data = self.process_job_with_multi_model(job)
                    if proposal_data is not None:
                        self.save_to_queue(proposal_data)
                        self.save_proposal_html(proposal_data)
                        processed_count += 1
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success", 
                    "total_jobs": len(jobs),
                    "processed": processed_count,
                    "rejected": len(jobs) - processed_count,
                    "ai_models_used": {
                        "openai": OPENAI_AVAILABLE,
                        "gemini": True,
                        "cohere": COHERE_AVAILABLE
                    }
                }).encode())
                
            except Exception as e:
                self.send_error(500, f"Error processing jobs: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found")
    
    def process_job_with_multi_model(self, job):
        """Process job with multi-model AI system"""
        
        # Extract job details
        job_title = job.get('title', 'Untitled Job')
        job_description = job.get('description', '')
        budget = job.get('budget', 'Not specified')
        client_name = self.extract_client_name(job)
        
        # Generate consistent timestamp
        timestamp = int(time.time() * 1000)
        
        # Enhanced scoring system
        job_analysis = self.analyze_job_advanced(job_title, job_description)
        
        # Check if job was rejected
        if job_analysis.get('rejected', False):
            print(f"🚫 MULTI-MODEL REJECTED: {job_title[:50]}... | Reason: {job_analysis.get('reason', 'Unknown')}")
            return None
        
        # Generate proposal with multi-model AI
        proposal_message = self.generate_proposal_multi_model(
            job_title, job_description, budget, job_analysis
        )
        
        # Generate filename
        filename = self.generate_filename_with_timestamp(job_title, timestamp)
        
        # Create enhanced proposal data
        proposal_data = {
            "job_id": job.get('guid', f"job_{timestamp}"),
            "job_title": job_title,
            "client_name": client_name,
            "budget": budget,
            "description": job_description[:500] + "..." if len(job_description) > 500 else job_description,
            "analysis": job_analysis,
            "message": proposal_message,
            "score": job_analysis.get('score', 75),
            "created_at": datetime.now().isoformat(),
            "proposal_url": f"https://proposals.projekt-ai.net/{filename}",
            "original_job_url": job.get('link', ''),
            "status": "pending",
            "filename": filename,
            "automation_terms_found": job_analysis.get('automation_terms_found', 0),
            "specialties": job_analysis.get('specialties', []),
            "ai_model_used": job_analysis.get('ai_model_used', 'multi-model'),
            "server_version": "multi-model-test"
        }
        
        return proposal_data
    
    def generate_proposal_multi_model(self, job_title, job_description, budget, analysis):
        """Generate proposal using multi-model AI system"""
        
        print(f"🤖 MULTI-MODEL AI: Generating proposal for {job_title[:30]}...")
        
        # Try GPT-4 first (primary model)
        if OPENAI_AVAILABLE:
            try:
                proposal = self.generate_with_gpt4(job_title, job_description, budget, analysis)
                if proposal:
                    print(f"✅ GPT-4 generated proposal")
                    analysis['ai_model_used'] = 'gpt-4'
                    return proposal
            except Exception as e:
                print(f"⚠️ GPT-4 failed: {e}")
        
        # Fallback to Gemini (secondary)
        try:
            proposal = self.generate_with_gemini(job_title, job_description, budget, analysis)
            if proposal:
                print(f"✅ Gemini generated proposal")
                analysis['ai_model_used'] = 'gemini-2.0-flash'
                return proposal
        except Exception as e:
            print(f"⚠️ Gemini failed: {e}")
        
        # Final fallback
        analysis['ai_model_used'] = 'fallback'
        return self.generate_fallback_proposal(job_title, analysis)
    
    def generate_with_gpt4(self, job_title, job_description, budget, analysis):
        """Generate proposal using GPT-4"""
        
        if not OPENAI_AVAILABLE:
            return None
            
        prompt = f"""You are Timothy Poulton, a 20-year automation specialist. Write a personalized Upwork proposal.

Job: {job_title}
Budget: {budget}
Description: {job_description[:500]}
Pain Points: {', '.join(analysis.get('pain_points', ['automation needs']))}

Write a 100-150 word proposal that:
1. References their specific challenge
2. Shares relevant experience (no fake stats)
3. Outlines 2-3 step approach
4. Natural closing

Sound genuine, not templated. Use "I" statements."""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"GPT-4 error: {e}")
            return None
    
    def generate_with_gemini(self, job_title, job_description, budget, analysis):
        """Generate proposal using Gemini"""
        
        prompt = f"""You are Timothy Poulton, a 20-year automation specialist. Write a personalized Upwork proposal.

Job: {job_title}
Budget: {budget}
Description: {job_description[:500]}
Pain Points: {', '.join(analysis.get('pain_points', ['automation needs']))}

Write a 100-150 word proposal that:
1. References their specific challenge
2. Shares relevant experience (no fake stats)
3. Outlines 2-3 step approach
4. Natural closing

Sound genuine, not templated."""
        
        try:
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
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                return None
                
        except Exception as e:
            print(f"Gemini error: {e}")
            return None
    
    def analyze_job_advanced(self, title, description):
        """Advanced job analysis using scoring-config.json"""
        
        # Load advanced scoring configuration
        scoring_config_path = os.path.join(os.path.dirname(__file__), 'scoring-config.json')
        try:
            with open(scoring_config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"⚠️ Scoring config error: {e}")
            return self.analyze_job_simple(title, description)
        
        text = f"{title} {description}".lower()
        score = 70  # Base score
        
        print(f"🔍 ADVANCED SCORING: Analyzing '{title[:30]}...'")
        
        # Check immediate disqualifiers
        immediate_disqualifiers = config['scoring_rules']['negative_keywords']['immediate_disqualifiers']['terms']
        for term in immediate_disqualifiers:
            if term.lower() in text:
                return {
                    'score': 0,
                    'rejected': True,
                    'reason': f"Disqualified: {term}",
                    'analysis_type': 'advanced'
                }
        
        # Check automation requirements
        automation_terms = config['filtering']['required_automation_terms']['terms']
        automation_count = sum(1 for term in automation_terms if term.lower() in text)
        min_required = config['filtering']['required_automation_terms']['minimum_required']
        
        if automation_count < min_required:
            return {
                'score': 0,
                'rejected': True,
                'reason': f"Only {automation_count}/{min_required} automation terms",
                'analysis_type': 'advanced'
            }
        
        # Apply positive scoring
        keywords = config['scoring_rules']['keywords']
        tools_found = []
        specialties = []
        
        # AI automation bonus
        for term in keywords['ai_automation']['terms']:
            if term.lower() in text:
                score += keywords['ai_automation']['points']
                break
        
        # Primary tools
        for term in keywords['primary_tools']['terms']:
            if term.lower() in text:
                score += keywords['primary_tools']['points']
                tools_found.append(term.title())
                break
        
        # Timothy's specialties
        for term in keywords['timothy_specialties']['terms']:
            if term.lower() in text:
                score += keywords['timothy_specialties']['points']
                specialties.append(term)
                break
        
        print(f"✅ ADVANCED SCORE: {score} - {automation_count} automation terms")
        
        return {
            'score': min(score, 100),
            'rejected': False,
            'automation_terms_found': automation_count,
            'tools': tools_found or ['Automation Tools'],
            'specialties': specialties,
            'pain_points': self.extract_pain_points(text),
            'industry': self.detect_industry(text),
            'analysis_type': 'advanced'
        }
    
    def analyze_job_simple(self, title, description):
        """Simple fallback analysis"""
        text = f"{title} {description}".lower()
        score = 75
        
        # Basic automation check
        automation_keywords = ['automat', 'integrat', 'workflow', 'api']
        if any(keyword in text for keyword in automation_keywords):
            score += 10
        
        return {
            'score': score,
            'rejected': False,
            'tools': ['Automation Platform'],
            'pain_points': ['workflow optimization'],
            'industry': 'general business',
            'analysis_type': 'simple'
        }
    
    def extract_pain_points(self, text):
        """Extract pain points from job description"""
        pain_keywords = {
            'manual': 'manual processes',
            'time-consuming': 'time-consuming tasks',
            'repetitive': 'repetitive work',
            'integrate': 'integration challenges',
            'automate': 'automation needs'
        }
        
        found_points = []
        for keyword, pain in pain_keywords.items():
            if keyword in text:
                found_points.append(pain)
        
        return found_points or ['workflow optimization']
    
    def detect_industry(self, text):
        """Detect industry from job description"""
        if any(term in text for term in ['restaurant', 'hospitality', 'venue']):
            return 'hospitality'
        elif any(term in text for term in ['ecommerce', 'online store']):
            return 'e-commerce'
        elif any(term in text for term in ['saas', 'software']):
            return 'SaaS'
        else:
            return 'general business'
    
    def extract_client_name(self, job):
        """Extract client name from job data"""
        client = job.get('client', {})
        if isinstance(client, dict):
            return client.get('name', 'Client')
        elif isinstance(client, str):
            return client
        return job.get('client_name', 'Potential Client')
    
    def generate_fallback_proposal(self, job_title, analysis):
        """Fallback proposal if all AI models fail"""
        return f"""I see you need help with automation for your project.

With 20 years in automation, I can streamline your workflows using the right tools for your needs.

My approach:
1. Analyze your current process
2. Design custom automation workflow
3. Implement and test the solution

I'd be happy to discuss your specific requirements. When would be a good time for a brief call?

Best,
Timothy"""
    
    def save_to_queue(self, proposal_data):
        """Save proposal to queue (same as original)"""
        queue_file = QUEUE_FILE
        
        try:
            if os.path.exists(queue_file):
                with open(queue_file, 'r') as f:
                    queue = json.load(f)
            else:
                queue = []
            
            queue.append(proposal_data)
            queue = queue[-100:]  # Keep last 100
            
            with open(queue_file, 'w') as f:
                json.dump(queue, f, indent=2)
                
        except Exception as e:
            print(f"Error saving to queue: {e}")
    
    def save_proposal_html(self, proposal_data):
        """Save proposal as HTML (simplified for testing)"""
        filename = proposal_data.get('filename')
        if not filename:
            return
            
        filepath = os.path.join(PROPOSALS_DIR, filename)
        
        # Simple HTML for testing
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{proposal_data['job_title']}</title>
    <style>body {{ font-family: Arial; margin: 40px; }}</style>
</head>
<body>
    <h1>MULTI-MODEL AI PROPOSAL</h1>
    <h2>{proposal_data['job_title']}</h2>
    <p><strong>Client:</strong> {proposal_data['client_name']}</p>
    <p><strong>Budget:</strong> {proposal_data['budget']}</p>
    <p><strong>Score:</strong> {proposal_data['score']}</p>
    <p><strong>AI Model:</strong> {proposal_data.get('ai_model_used', 'multi-model')}</p>
    <div style="background:#f5f5f5; padding:20px; margin:20px 0;">
        <h3>Proposal:</h3>
        <p>{proposal_data['message']}</p>
    </div>
    <p><em>Generated by Multi-Model AI System on port {PORT}</em></p>
</body>
</html>"""
        
        try:
            os.makedirs(PROPOSALS_DIR, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(html_content)
            print(f"✅ Multi-model proposal saved: {filename}")
        except Exception as e:
            print(f"Error saving HTML: {e}")
    
    def generate_filename_with_timestamp(self, job_title, timestamp):
        """Generate filename with timestamp"""
        safe_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_'))
        safe_title = safe_title.replace(' ', '-')[:50]
        return f"proposal-multimodel-{safe_title}-{timestamp}.html"

def run_server():
    """Run the multi-model test server"""
    
    print(f"🚀 MULTI-MODEL AI TEST SERVER")
    print(f"📡 Port: {PORT} (temporary testing)")
    print(f"🤖 AI Models Available:")
    print(f"   • OpenAI GPT-4: {'✅' if OPENAI_AVAILABLE else '❌'}")
    print(f"   • Gemini 2.0 Flash: ✅")
    print(f"   • Cohere: {'✅' if COHERE_AVAILABLE else '❌'}")
    print(f"📊 Status endpoint: http://192.168.1.107:{PORT}/status")
    print(f"🔗 Test webhook: http://192.168.1.107:{PORT}/webhook/rss-jobs")
    
    with ReusableUpworkServer(("", PORT), UpworkProposalServer) as httpd:
        print(f"✅ Multi-model test server running!")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server() 