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
PROPOSALS_DIR = "/var/www/projekt-ai.net/proposals/"  # Updated to correct directory
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
        elif self.path == '/data/proposals.json':
            # Dashboard endpoint - serve proposals in expected format
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            
            try:
                with open(QUEUE_FILE, 'r') as f:
                    proposals = json.load(f)
                    # Sort by timestamp (most recent first)
                    if isinstance(proposals, list):
                        proposals.sort(key=lambda x: x.get('timestamp', x.get('created_at', '')), reverse=True)
                    
                    # Format for dashboard with anti-cache headers
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
        """Handle POST requests for proposal management"""
        if self.path.startswith('/api/proposals/'):
            # Extract job_id from path
            job_id = self.path.split('/')[-2]  # /api/proposals/{job_id}/status
            action = self.path.split('/')[-1]  # status, edit, etc.
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                if action == 'status':
                    # Update proposal status
                    new_status = data.get('status')
                    if new_status in ['pending', 'approved', 'rejected']:
                        success = self.update_proposal_status(job_id, new_status)
                        if success:
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.send_header('Access-Control-Allow-Origin', '*')
                            self.end_headers()
                            self.wfile.write(json.dumps({
                                "status": "success",
                                "action": f"status_updated_to_{new_status}"
                            }).encode())
                        else:
                            self.send_error(404, "Proposal not found")
                    else:
                        self.send_error(400, "Invalid status")
                
                elif action == 'edit':
                    # Handle proposal edit/regeneration
                    feedback = data.get('feedback', '')
                    if feedback:
                        # Get original proposal
                        with open(QUEUE_FILE, 'r') as f:
                            proposals = json.load(f)
                            proposal = next((p for p in proposals if p.get('job_id') == job_id), None)
                        
                        if proposal:
                            # Regenerate proposal with feedback
                            new_proposal = self.regenerate_proposal(proposal, feedback)
                            if new_proposal:
                                # Update in queue
                                self.update_proposal_in_queue(job_id, new_proposal)
                                
                                self.send_response(200)
                                self.send_header('Content-type', 'application/json')
                                self.send_header('Access-Control-Allow-Origin', '*')
                                self.end_headers()
                                self.wfile.write(json.dumps({
                                    "status": "success",
                                    "action": "proposal_regenerated",
                                    "proposal": new_proposal
                                }).encode())
                            else:
                                self.send_error(500, "Failed to regenerate proposal")
                        else:
                            self.send_error(404, "Proposal not found")
                    else:
                        self.send_error(400, "Feedback required for edit")
                
                else:
                    self.send_error(404, "Invalid action")
                    
            except Exception as e:
                self.send_error(500, f"Error processing request: {str(e)}")
        
        elif self.path == '/webhook/job-direct':
            # New endpoint for direct job processing from the simple generator
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Process a single job
                job = json.loads(post_data)
                
                # Prepare job format to match what process_job_with_multi_model expects
                # Map job_title to title for compatibility
                formatted_job = {
                    'title': job.get('job_title', job.get('title', '')),  # Support both field names
                    'description': job.get('description', ''),
                    'budget': job.get('budget', 'Not specified'),
                    'link': job.get('url', job.get('original_job_url', '')),
                    'guid': job.get('job_id', f"direct_{int(time.time() * 1000)}")
                }
                
                # Add client name if provided
                if 'client_name' in job:
                    formatted_job['client'] = {'name': job.get('client_name')}
                
                # Process the job
                proposal_data = self.process_job_with_multi_model(formatted_job)
                
                if proposal_data is not None:
                    # Save the proposal HTML file
                    self.save_proposal_html(proposal_data)
                    
                    # Send success response with the proposal data
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(proposal_data).encode())
                else:
                    # Job was rejected by the scoring system
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "rejected",
                        "job_title": job.get('job_title', job.get('title', 'Unknown Job')),
                        "message": "This job doesn't match your criteria or wasn't suitable for automation.",
                        "score": 0
                    }).encode())
                
            except Exception as e:
                self.send_error(500, f"Error processing direct job: {str(e)}")
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
        
        # Generate proposal sections
        proposal_sections = self.generate_proposal_multi_model(job_title, job_description, budget, job_analysis)
        
        # Generate filename
        filename = self.generate_filename_with_timestamp(job_title, timestamp)
        
        # Create enhanced proposal data - ALWAYS include original job data
        proposal_data = {
            "job_id": job.get('guid', f"job_{timestamp}"),
            "job_title": job_title,  # Always preserve original title
            "client_name": client_name,
            "budget": budget,
            "description": job_description[:500] + "..." if len(job_description) > 500 else job_description,
            "analysis": job_analysis,
            "proposal_sections": proposal_sections,
            "score": job_analysis.get('score', 75),
            "created_at": datetime.now().isoformat(),
            "proposal_url": f"https://proposals.projekt-ai.net/proposals/{filename}",
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
        print(f"🤖 MULTI-MODEL AI: Generating proposal for {job_title[:30]}...")
        # Try GPT-4 first (primary model)
        if OPENAI_AVAILABLE:
            try:
                proposal_sections = self.generate_with_gpt4(job_title, job_description, budget, analysis)
                if self.is_valid_proposal(proposal_sections):
                    print(f"✅ GPT-4 generated proposal sections")
                    analysis['ai_model_used'] = 'gpt-4'
                    return proposal_sections
            except Exception as e:
                print(f"⚠️ GPT-4 failed: {e}")
        # Fallback to Gemini (secondary)
        try:
            proposal_sections = self.generate_with_gemini(job_title, job_description, budget, analysis)
            if self.is_valid_proposal(proposal_sections):
                print(f"✅ Gemini generated proposal sections")
                analysis['ai_model_used'] = 'gemini-2.0-flash'
                return proposal_sections
        except Exception as e:
            print(f"⚠️ Gemini failed: {e}")
        # Fallback to Cohere (if implemented)
        # try:
        #     proposal_sections = self.generate_with_cohere(job_title, job_description, budget, analysis)
        #     if self.is_valid_proposal(proposal_sections):
        #         print(f"✅ Cohere generated proposal sections")
        #         analysis['ai_model_used'] = 'cohere'
        #         return proposal_sections
        # except Exception as e:
        #     print(f"⚠️ Cohere failed: {e}")
        error_msg = f"ERROR: No valid proposal generated by any AI model for job: {job_title}"
        print(error_msg)
        return {"error": error_msg}

    def is_valid_proposal(self, proposal):
        required_keys = ["current_process", "automated_solution", "technical_roadmap", "technologies_used", "automated_workflow", "about_me", "whats_included"]
        if not proposal or not isinstance(proposal, dict):
            return False
        for key in required_keys:
            if key not in proposal or not proposal[key].strip():
                return False
        return True

    def generate_with_gpt4(self, job_title, job_description, budget, analysis):
        """Generate proposal using GPT-4"""
        try:
            client = openai.OpenAI(api_key=openai.api_key)
            about_me = ("I'm Timothy Poulton, and my experience spans 20 years across the nightlife, music and hospitality industries. "
                        "I've watched the same problems crush brilliant business owners: manual processes consuming countless hours daily, staff burnout from repetitive tasks, and revenue opportunities missed because you're stuck managing operations instead of growing your business.\n\n"
                        "Here's what I know: The best businesses aren't just offering great experiences—they're using intelligent automation to deliver them consistently while their competitors are still drowning in spreadsheets.")
            prompt = f"""
You are Timothy Poulton, a 20-year automation specialist and solo freelancer. Write a detailed Upwork proposal for the following job. Structure your response as JSON with these keys:

- current_process: Describe the client's current/manual process as inferred from the job post.
- automated_solution: Describe your proposed automation solution, referencing the job post.
- technical_roadmap: Concise but detailed breakdown of your intended solution.
- technologies_used: List the tools and software you would use.
- automated_workflow: Step-by-step or visual workflow of how the solution would work.
- about_me: Use this text verbatim: '{about_me}'
- whats_included: List what the client will receive.

**Do not leave any section blank. If you cannot infer a section, make a best guess based on the job description.**

Return ONLY valid JSON with those keys, no extra commentary. Here is an example schema:

{{
  "current_process": "...",
  "automated_solution": "...",
  "technical_roadmap": "...",
  "technologies_used": "...",
  "automated_workflow": "...",
  "about_me": "...",
  "whats_included": "..."
}}

Job Title: {job_title}
Budget: {budget}
Description: {job_description[:500]}
"""
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional automation expert with 20 years experience."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=900
            )
            import json as pyjson
            content = response.choices[0].message.content.strip()
            try:
                parsed = pyjson.loads(content)
                if self.is_valid_proposal(parsed):
                    return parsed
                else:
                    print(f"Invalid proposal structure. Raw AI output: {content}")
                    return None
            except Exception:
                print(f"JSON parse error. Raw AI output: {content}")
                return None
        except Exception as e:
            print(f"GPT-4 error: {str(e)}")
            return None
    
    def generate_with_gemini(self, job_title, job_description, budget, analysis):
        """Generate proposal using Gemini"""
        about_me = ("I'm Timothy Poulton, and my experience spans 20 years across the nightlife, music and hospitality industries. "
                    "I've watched the same problems crush brilliant business owners: manual processes consuming countless hours daily, staff burnout from repetitive tasks, and revenue opportunities missed because you're stuck managing operations instead of growing your business.\n\n"
                    "Here's what I know: The best businesses aren't just offering great experiences—they're using intelligent automation to deliver them consistently while their competitors are still drowning in spreadsheets.")
        prompt = f"""
You are Timothy Poulton, a 20-year automation specialist. Write a detailed Upwork proposal for the following job. Structure your response as JSON with these keys:

- current_process: Describe the client's current/manual process as inferred from the job post.
- automated_solution: Describe your proposed automation solution, referencing the job post.
- technical_roadmap: Concise but detailed breakdown of your intended solution.
- technologies_used: List the tools and software you would use.
- automated_workflow: Step-by-step or visual workflow of how the solution would work.
- about_me: Use this text verbatim: '{about_me}'
- whats_included: List what the client will receive.

**Do not leave any section blank. If you cannot infer a section, make a best guess based on the job description.**

Return ONLY valid JSON with those keys, no commentary. Here is an example schema:

{{
  "current_process": "...",
  "automated_solution": "...",
  "technical_roadmap": "...",
  "technologies_used": "...",
  "automated_workflow": "...",
  "about_me": "...",
  "whats_included": "..."
}}

Job Title: {job_title}
Budget: {budget}
Description: {job_description[:500]}
"""
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
                import json as pyjson
                content = result['candidates'][0]['content']['parts'][0]['text'].strip()
                try:
                    parsed = pyjson.loads(content)
                    if self.is_valid_proposal(parsed):
                        return parsed
                    else:
                        print(f"Invalid proposal structure. Raw AI output: {content}")
                        return None
                except Exception:
                    print(f"JSON parse error. Raw AI output: {content}")
                    return None
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
    
    def update_proposal_status(self, job_id, new_status):
        """Update proposal status in queue"""
        try:
            if os.path.exists(QUEUE_FILE):
                with open(QUEUE_FILE, 'r') as f:
                    proposals = json.load(f)
            else:
                return False
            
            # Find and update the proposal
            updated = False
            for proposal in proposals:
                if proposal.get('job_id') == job_id:
                    proposal['status'] = new_status
                    proposal['updated_at'] = datetime.now().isoformat()
                    updated = True
                    break
            
            if updated:
                # Save updated queue
                with open(QUEUE_FILE, 'w') as f:
                    json.dump(proposals, f, indent=2)
                
                # Update web data
                self.sync_web_data(proposals)
                print(f"✅ Updated proposal {job_id} status to {new_status}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating proposal status: {e}")
            return False

    def regenerate_proposal(self, original_proposal, feedback):
        """Regenerate proposal with feedback using multi-model AI"""
        try:
            # Prepare job data for regeneration
            job_data = {
                'title': original_proposal.get('job_title', ''),
                'description': original_proposal.get('description', ''),
                'budget': original_proposal.get('budget', ''),
                'client': {'name': original_proposal.get('client_name', '')},
                'edit_feedback': feedback,
                'original_proposal': original_proposal.get('message', '')
            }
            
            # Process with multi-model AI
            proposal_data = self.process_job_with_multi_model(job_data)
            
            if proposal_data:
                # Preserve original metadata
                proposal_data.update({
                    'job_id': original_proposal.get('job_id'),
                    'created_at': original_proposal.get('created_at'),
                    'updated_at': datetime.now().isoformat(),
                    'status': 'pending',  # Reset status for review
                    'edit_count': original_proposal.get('edit_count', 0) + 1,
                    'edit_history': original_proposal.get('edit_history', []) + [{
                        'timestamp': datetime.now().isoformat(),
                        'feedback': feedback
                    }]
                })
                return proposal_data
            
            return None
            
        except Exception as e:
            print(f"Error regenerating proposal: {e}")
            return None

    def update_proposal_in_queue(self, job_id, new_proposal):
        """Update proposal in queue with new version"""
        try:
            if os.path.exists(QUEUE_FILE):
                with open(QUEUE_FILE, 'r') as f:
                    proposals = json.load(f)
            else:
                return False
            
            # Find and update the proposal
            updated = False
            for i, proposal in enumerate(proposals):
                if proposal.get('job_id') == job_id:
                    proposals[i] = new_proposal
                    updated = True
                    break
            
            if updated:
                # Save updated queue
                with open(QUEUE_FILE, 'w') as f:
                    json.dump(proposals, f, indent=2)
                
                # Update web data
                self.sync_web_data(proposals)
                print(f"✅ Updated proposal {job_id} with new version")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating proposal in queue: {e}")
            return False

    def sync_web_data(self, proposals):
        """Sync proposal data to web directory"""
        try:
            # Format web data
            web_data = {
                "proposals": proposals,
                "generated_at": datetime.now().isoformat(),
                "total_count": len(proposals)
            }
            
            # Save to web directory for dashboard
            web_file = "/var/www/projekt-ai.net/data/proposals.json"
            os.makedirs(os.path.dirname(web_file), exist_ok=True)
            
            with open(web_file, 'w') as f:
                json.dump(web_data, f, indent=2)
            
            print(f"✅ Updated web data file with {len(proposals)} proposals")
            return True
            
        except Exception as e:
            print(f"⚠️ Warning: Failed to update web data: {e}")
            return False
    
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
        # Before saving, check for error in proposal
        if 'error' in proposal_data:
            print(f"Proposal not saved: {proposal_data['error']}")
            return False
        filename = proposal_data.get('filename')
        if not filename:
            return
        filepath = os.path.join(PROPOSALS_DIR, filename)
        
        # Use the verified dark template
        template_path = "/var/www/projekt-ai.net/templates/dark-proposal-template.html"
        try:
            with open(template_path, 'r') as f:
                template = f.read()
        except Exception as e:
            print(f"Error loading dark template: {e}")
            return
        # Use clientCountry or clientLocation as client_name if available
        client_name = proposal_data.get('client_name')
        if not client_name:
            client_name = proposal_data.get('clientCountry') or proposal_data.get('clientLocation', 'Valued Client')
        
        sections = proposal_data.get('proposal_sections', {})
        
        # Map technologies/services to SERVICE_1...SERVICE_5
        techs = sections.get('technologies_used', [])
        if not isinstance(techs, list):
            print(f"Warning: technologies_used is not a list. Got: {type(techs)}. Value: {techs}")
            techs = []
        service_replacements = {}
        for i in range(5):
            service_replacements[f'[SERVICE_{i+1}]'] = techs[i] if i < len(techs) else ''
        
        # Map workflow steps
        steps = sections.get('automated_workflow_steps', [])
        if not isinstance(steps, list):
            print(f"Warning: automated_workflow_steps is not a list. Got: {type(steps)}. Value: {steps}")
            steps = []
        
        # Map icons, titles, and descriptions for the workflow
        step_replacements = {}
        for i in range(4):
            step = steps[i] if i < len(steps) else {}
            # Default workflow icons if not provided
            default_icons = ["⚡", "🔄", "🎯", "📊"]
            icon = step.get('icon', default_icons[i]) if isinstance(step, dict) else default_icons[i]
            step_replacements[f'[STEP_{i+1}_ICON]'] = icon
            step_replacements[f'[STEP_{i+1}_TITLE]'] = step.get('title', '') if isinstance(step, dict) else ''
            step_replacements[f'[STEP_{i+1}_DESC]'] = step.get('desc', '') if isinstance(step, dict) else ''
        
        # Map roadmap/process steps
        process = sections.get('technical_roadmap', [])
        if not isinstance(process, list):
            print(f"Warning: technical_roadmap is not a list. Got: {type(process)}. Value: {process}")
            process = []
        process_replacements = {}
        for i in range(4):
            proc = process[i] if i < len(process) else {}
            process_replacements[f'[PROCESS_{i+1}_TITLE]'] = proc.get('title', '') if isinstance(proc, dict) else ''
            process_replacements[f'[PROCESS_{i+1}_DESC]'] = proc.get('desc', '') if isinstance(proc, dict) else ''
        
        # Format what's included as a list
        whats_included = sections.get('whats_included', [])
        if not isinstance(whats_included, list):
            print(f"Warning: whats_included is not a list. Got: {type(whats_included)}. Value: {whats_included}")
            whats_included = [whats_included] if whats_included else []
        
        # Main replacements
        replacements = {
            '[CLIENT_NAME]': client_name,
            '[PROJECT_TITLE]': proposal_data.get('job_title', ''),
            '[PROJECT_SUBTITLE]': 'Transform your manual processes with intelligent automation workflows',
            '[WORKFLOW_SUBTITLE]': 'Streamline your operations with smart automation',
            '[CURRENT_PROCESS]': sections.get('current_process', ''),
            '[DESIRED_OUTCOME]': sections.get('automated_solution', ''),
            # Remove stats
            '[STAT_1_VALUE]': '', 
            '[STAT_1_LABEL]': '',
            '[STAT_2_VALUE]': '',
            '[STAT_2_LABEL]': '',
            '[STAT_3_VALUE]': '',
            '[STAT_3_LABEL]': '',
            # Remove pricing/timeline
            '[PRICE_RANGE]': '',
            '[DELIVERY_WEEKS]': '',
        }
        
        # Merge all replacements
        replacements.update(service_replacements)
        replacements.update(step_replacements)
        replacements.update(process_replacements)
        
        # Apply replacements
        html = template
        for k, v in replacements.items():
            if v is None:
                v = ''
            if not isinstance(v, str):
                v = str(v)
            html = html.replace(k, v)
        
        # Write the file
        with open(filepath, 'w') as f:
            f.write(html)
        
        print(f"✅ Multi-model proposal saved (dark theme): {filename}")
    
    def generate_filename_with_timestamp(self, job_title, timestamp):
        """Generate filename with timestamp"""
        safe_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_'))
        safe_title = safe_title.replace(' ', '-')[:50]
        return f"proposal-multimodel-{safe_title}-{timestamp}.html"

def run_server():
    """Run the multi-model production server"""
    
    print(f"🚀 MULTI-MODEL AI PRODUCTION SERVER")
    print(f"📡 Port: {PORT} (production)")
    print(f"🤖 AI Models Available:")
    print(f"   • OpenAI GPT-4: {'✅' if OPENAI_AVAILABLE else '❌'}")
    print(f"   • Gemini 2.0 Flash: ✅")
    print(f"   • Cohere: {'✅' if COHERE_AVAILABLE else '❌'}")
    print(f"📊 Status endpoint: http://192.168.1.107:{PORT}/status")
    print(f"🔗 Webhook: http://192.168.1.107:{PORT}/webhook/rss-jobs")
    print(f"📋 Queue file: {QUEUE_FILE}")
    print(f"📁 Proposals dir: {PROPOSALS_DIR}")
    
    with ReusableUpworkServer(("", PORT), UpworkProposalServer) as httpd:
        print(f"✅ Multi-model production server running!")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server() 