#!/usr/bin/env python3
"""
Upwork Proposal Automation Server - FIXED VERSION
A simple, all-in-one solution for generating HTML proposals from Upwork jobs
FIXES: OpenAI API v1.0+, Client Name Extraction, Enhanced Fallbacks
"""

import http.server
import socketserver
import json
import os
import re
from datetime import datetime, timedelta
from urllib.parse import parse_qs
import threading
import time
from openai import OpenAI

# Configure OpenAI API v1.0+
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))

# Load scoring configuration
SCORING_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'scoring-config.json')
SCORING_CONFIG = {}

try:
    with open(SCORING_CONFIG_PATH, 'r') as f:
        SCORING_CONFIG = json.load(f)
except:
    print("⚠️ No scoring config found, using basic scoring")

class UpworkProposalServer(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle incoming webhook from Upwork Job Scraper"""
        if self.path == '/webhook/rss-jobs':
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Handle both formats: direct list or wrapped in {jobs: [...]}
                if isinstance(data, list):
                    jobs = data  # Direct list format
                elif isinstance(data, dict):
                    jobs = data.get('jobs', [])  # Wrapped format
                else:
                    jobs = []
                
                results = []
                
                for job in jobs:
                    # Score the job
                    score = self.calculate_job_score(job)
                    
                    # Get thresholds from config
                    thresholds = SCORING_CONFIG.get('thresholds', {'consider': 40})
                    min_threshold = thresholds.get('consider', 40)
                    
                    # Determine priority level
                    priority = 'skip'
                    if score >= thresholds.get('must_apply', 80):
                        priority = 'must_apply'
                    elif score >= thresholds.get('should_apply', 60):
                        priority = 'should_apply'
                    elif score >= thresholds.get('consider', 40):
                        priority = 'consider'
                    
                    # Generate proposal if score meets minimum threshold
                    if score >= min_threshold:
                        proposal_data = self.generate_proposal(job, score)
                        proposal_data['priority'] = priority
                        results.append(proposal_data)
                        
                        # Save to review queue
                        self.save_to_queue(proposal_data)
                        
                        print(f"\n✅ Generated proposal: {priority.upper()} priority (Score: {score})")
                    else:
                        print(f"\n❌ Skipped job (Score: {score}): {job.get('title', 'Unknown')[:50]}...")
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'success': True,
                    'processed': len(jobs),
                    'proposals_generated': len(results)
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_error(500, str(e))
    
    def calculate_job_score(self, job):
        """Advanced job scoring using configuration"""
        if not SCORING_CONFIG:
            return self.calculate_job_score_basic(job)
        
        score = 0
        score_breakdown = []
        
        rules = SCORING_CONFIG.get('scoring_rules', {})
        
        # 1. Budget scoring
        budget = self.extract_budget(job)
        if budget:
            for budget_range in rules.get('budget', {}).get('ranges', []):
                if budget >= budget_range['min'] and (budget_range['max'] is None or budget <= budget_range['max']):
                    score += budget_range['points']
                    score_breakdown.append(f"Budget {budget_range['label']}: +{budget_range['points']}")
                    break
        
        # Check if hourly rate
        if 'hourly' in str(job.get('budget', '')).lower():
            hourly_config = rules.get('budget', {}).get('hourly_rate', {})
            # Extract hourly rate if available
            hourly_match = re.search(r'\$(\d+)(?:-\$?\d+)?/hr', str(job.get('budget', '')))
            if hourly_match:
                hourly_rate = int(hourly_match.group(1))
                min_rate = hourly_config.get('min_rate', 50)
                if hourly_rate >= min_rate:
                    bonus = min((hourly_rate - min_rate) // 10 * hourly_config.get('points_per_10_above_min', 5), 
                               hourly_config.get('max_points', 30))
                    score += bonus
                    score_breakdown.append(f"Hourly rate ${hourly_rate}/hr: +{bonus}")
        
        # 2. Keyword scoring
        description = (job.get('title', '') + ' ' + job.get('description', '')).lower()
        
        for category, config in rules.get('keywords', {}).items():
            points = config.get('points', 0)
            for term in config.get('terms', []):
                if term.lower() in description:
                    score += points
                    score_breakdown.append(f"{category} keyword '{term}': +{points}")
                    break  # Only count once per category
        
        # 3. Negative keywords
        for category, config in rules.get('negative_keywords', {}).items():
            points = config.get('points', 0)
            for term in config.get('terms', []):
                if term.lower() in description:
                    score += points  # points are negative
                    score_breakdown.append(f"Negative keyword '{term}': {points}")
        
        # 4. Client quality scoring
        client_data = job.get('client', {})
        client_rules = rules.get('client_quality', {})
        
        # Payment verified
        if client_data.get('paymentVerified') and client_rules.get('payment_verified', {}).get('points'):
            points = client_rules['payment_verified']['points']
            score += points
            score_breakdown.append(f"Payment verified: +{points}")
        
        # Client spending
        total_spent = client_data.get('totalSpent', 0)
        for tier in client_rules.get('spending_tiers', []):
            if total_spent >= tier['min']:
                score += tier['points']
                score_breakdown.append(f"{tier['label']}: +{tier['points']}")
                break
        
        # Hire rate
        jobs_posted = client_data.get('totalJobsPosted', 1)
        hires = client_data.get('totalHires', 0)
        if jobs_posted > 0:
            hire_rate = (hires / jobs_posted) * 100
            if hire_rate >= client_rules.get('hire_rate', {}).get('min_percentage', 80):
                points = client_rules['hire_rate']['points']
                score += points
                score_breakdown.append(f"Hire rate {hire_rate:.0f}%: +{points}")
        
        # Average rating
        avg_rating = client_data.get('avgHourlyRate', 0)
        if avg_rating >= client_rules.get('average_rating', {}).get('min_rating', 4.8):
            points = client_rules['average_rating']['points']
            score += points
            score_breakdown.append(f"Client rating {avg_rating}: +{points}")
        
        # Location
        location = client_data.get('location', {}).get('country', '')
        if location in client_rules.get('location_preference', {}).get('preferred', []):
            points = client_rules['location_preference']['points']
            score += points
            score_breakdown.append(f"Preferred location {location}: +{points}")
        
        # 5. Competition analysis
        competition_rules = rules.get('competition', {})
        
        # Number of proposals
        proposals_count = job.get('proposalsCount', 0)
        for range_config in competition_rules.get('proposals_ranges', []):
            if proposals_count >= range_config['min'] and (range_config['max'] is None or proposals_count <= range_config['max']):
                score += range_config['points']
                score_breakdown.append(f"{range_config['label']} ({proposals_count} proposals): +{range_config['points']}")
                break
        
        # Time posted (fresher posts get higher score)
        posted_time = job.get('postedTime', '')
        if posted_time:
            try:
                # Calculate hours since posting
                now = datetime.now()
                posted = datetime.fromisoformat(posted_time.replace('Z', '+00:00'))
                hours_since_posting = (now - posted.replace(tzinfo=None)).total_seconds() / 3600
                
                for time_range in competition_rules.get('time_posted', []):
                    if hours_since_posting <= time_range.get('max_hours', float('inf')):
                        score += time_range['points']
                        score_breakdown.append(f"Posted {time_range['label']}: +{time_range['points']}")
                        break
            except:
                pass
        
        # Store breakdown for debugging
        job['score_breakdown'] = score_breakdown
        
        return score
    
    def extract_budget(self, job):
        """Extract budget amount from job posting"""
        budget_str = str(job.get('budget', ''))
        
        # Look for patterns like $500, $1,000, $1000-$5000
        budget_match = re.search(r'\$([0-9,]+)', budget_str)
        if budget_match:
            try:
                return int(budget_match.group(1).replace(',', ''))
            except:
                pass
        
        return 0
    
    def calculate_job_score_basic(self, job):
        """Basic scoring when no config is available"""
        score = 0
        
        # Budget scoring
        budget = self.extract_budget(job)
        if budget >= 5000:
            score += 40
        elif budget >= 2000:
            score += 25
        elif budget >= 1000:
            score += 15
        elif budget >= 500:
            score += 5
        
        # Keyword scoring
        description = (job.get('title', '') + ' ' + job.get('description', '')).lower()
        
        automation_keywords = ['automation', 'workflow', 'integrate', 'api', 'zapier', 'n8n', 'make.com']
        for keyword in automation_keywords:
            if keyword in description:
                score += 10
                break
        
        # Negative keywords
        negative_keywords = ['wordpress', 'website design', 'logo', 'graphic', 'mobile app']
        for keyword in negative_keywords:
            if keyword in description:
                score -= 20
                break
        
        return score
    
    def extract_client_name(self, job):
        """Extract client name from job posting with intelligent fallbacks"""
        client_data = job.get('client', {})
        
        # Try multiple sources for client name
        possible_names = []
        
        # 1. Direct client name field
        if client_data.get('name'):
            possible_names.append(client_data['name'])
        
        # 2. Extract from description patterns
        description = job.get('description', '')
        
        # Look for "I'm [name]", "We are [company]", "My name is [name]"
        name_patterns = [
            r"I'?m ([A-Z][a-z]+ ?[A-Z]?[a-z]*)",
            r"My name is ([A-Z][a-z]+ ?[A-Z]?[a-z]*)",
            r"We are ([A-Z][A-Za-z\s&]+?)(?:\.|,|\s+and|\s+looking)",
            r"(?:Our|My) company (?:is )?([A-Z][A-Za-z\s&]+?)(?:\.|,|\s+and|\s+looking)",
            r"at ([A-Z][A-Za-z\s&]+?)(?:,| we| and)"
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, description)
            if matches:
                possible_names.extend(matches)
        
        # 3. Extract from email signature patterns
        email_pattern = r"([A-Z][a-z]+)\s+([A-Z][a-z]+)\s*\n.*?@"
        email_matches = re.findall(email_pattern, description)
        if email_matches:
            possible_names.extend([f"{first} {last}" for first, last in email_matches])
        
        # 4. Clean and validate names
        clean_names = []
        for name in possible_names:
            name = name.strip()
            # Remove common false positives
            if len(name) > 2 and name not in ['Looking', 'Please', 'Thanks', 'Best', 'Regards', 'Team']:
                clean_names.append(name)
        
        # Return the first valid name or intelligent fallback
        if clean_names:
            return clean_names[0]
        
        # 5. Intelligent fallback based on context
        if 'team' in description.lower() or 'we are' in description.lower():
            return "Team"
        elif 'company' in description.lower():
            return "Company"
        else:
            return "Client"
    
    def generate_proposal(self, job, score):
        """Generate HTML proposal with enhanced AI analysis"""
        try:
            # Extract client name intelligently
            client_name = self.extract_client_name(job)
            
            # Analyze job with AI (enhanced version)
            analysis = self.analyze_job_with_ai_enhanced(job, score)
            
            # Generate job type
            job_type = self.extract_job_type(job.get('title', ''), job.get('description', ''))
            
            # Create filename
            safe_title = re.sub(r'[^a-zA-Z0-9\s]', '', job.get('title', 'proposal'))[:50]
            safe_title = re.sub(r'\s+', '-', safe_title.strip())
            filename = f"proposal-{safe_title}-{int(time.time())}.html"
            
            # Generate Upwork message
            message = self.generate_message(client_name, job_type, filename, score, analysis)
            
            # Load HTML template
            template_path = os.path.join(os.path.dirname(__file__), 'proposal-template.html')
            if not os.path.exists(template_path):
                self.create_default_template(template_path)
            
            with open(template_path, 'r') as f:
                html_template = f.read()
            
            # Replace template variables
            html_content = html_template.replace('{{CLIENT_NAME}}', client_name)
            html_content = html_content.replace('{{JOB_TITLE}}', job.get('title', ''))
            html_content = html_content.replace('{{JOB_BUDGET}}', job.get('budget', ''))
            html_content = html_content.replace('{{CURRENT_PROCESS}}', analysis.get('current_process', 'Current workflow'))
            html_content = html_content.replace('{{DESIRED_OUTCOME}}', analysis.get('desired_outcome', 'Improved efficiency'))
            html_content = html_content.replace('{{TOOLS}}', analysis.get('tools', 'Automation tools'))
            
            # Handle workflow steps
            workflow_steps_html = ''
            for i, step in enumerate(analysis.get('workflow_steps', []), 1):
                workflow_steps_html += f'''
                <div class="workflow-step">
                    <div class="step-number">{i}</div>
                    <div class="step-content">
                        <h4>{step.get('title', f'Step {i}')}</h4>
                        <p>{step.get('description', '')}</p>
                    </div>
                </div>
                '''
            html_content = html_content.replace('{{WORKFLOW_STEPS}}', workflow_steps_html)
            
            # Handle services list
            services_html = ''
            for service in analysis.get('services', []):
                services_html += f'<li>{service}</li>'
            html_content = html_content.replace('{{SERVICES}}', services_html)
            
            # Handle process items
            process_html = ''
            for item in analysis.get('process_items', []):
                process_html += f'''
                <div class="process-item">
                    <h4>{item.get('title', '')}</h4>
                    <p>{item.get('description', '')}</p>
                </div>
                '''
            html_content = html_content.replace('{{PROCESS_ITEMS}}', process_html)
            
            html_content = html_content.replace('{{UNIQUE_VALUE}}', analysis.get('unique_value', ''))
            html_content = html_content.replace('{{CUSTOM_APPROACH}}', analysis.get('custom_approach', ''))
            html_content = html_content.replace('{{SCORE}}', str(score))
            html_content = html_content.replace('{{TIMESTAMP}}', datetime.now().strftime('%Y-%m-%d %H:%M'))
            
            # Save HTML file
            output_dir = '/srv/apps/client-proposals/public/'
            os.makedirs(output_dir, exist_ok=True)
            
            with open(os.path.join(output_dir, filename), 'w') as f:
                f.write(html_content)
            
            return {
                'title': job.get('title', ''),
                'budget': job.get('budget', ''),
                'client_name': client_name,
                'score': score,
                'priority': 'standard',
                'filename': filename,
                'message': message,
                'url': f'https://projekt-ai.net/proposals/{filename}',
                'analysis': analysis,
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating proposal: {e}")
            return {
                'error': str(e),
                'title': job.get('title', ''),
                'score': score
            }
    
    def analyze_job_with_ai_enhanced(self, job, score):
        """Enhanced AI analysis with proper OpenAI v1.0+ API and better fallbacks"""
        if not client.api_key:
            return self.get_enhanced_fallback_content(job)
        
        try:
            # Determine AI depth based on score
            customization = SCORING_CONFIG.get('proposal_customization', {})
            
            ai_depth = 'standard'
            if score >= customization.get('high_score', {}).get('min_score', 80):
                ai_depth = customization['high_score'].get('ai_depth', 'comprehensive')
            elif score >= customization.get('medium_score', {}).get('min_score', 60):
                ai_depth = customization['medium_score'].get('ai_depth', 'standard')
            else:
                ai_depth = customization.get('low_score', {}).get('ai_depth', 'basic')
            
            # Adjust prompt based on depth
            depth_instructions = {
                'comprehensive': "Provide an extremely detailed, custom analysis with specific technical details, implementation timelines, and multiple solution options.",
                'standard': "Provide a professional analysis with clear steps and relevant solutions.",
                'basic': "Provide a concise, focused analysis highlighting key points."
            }
            
            prompt = f"""
            Analyze this Upwork job and provide custom proposal content.
            
            Job Title: {job.get('title', '')}
            Budget: {job.get('budget', '')}
            Description: {job.get('description', '')[:1000]}
            
            Analysis Depth: {ai_depth.upper()}
            Instructions: {depth_instructions.get(ai_depth, depth_instructions['standard'])}
            
            Return a JSON object with:
            - current_process: What the client is currently doing (1 sentence)
            - desired_outcome: What they want to achieve (1 sentence)
            - tools: Comma-separated list of tools/platforms mentioned or that would be useful
            - workflow_steps: Array of 4 steps, each with "title" and "description" fields
            - services: Array of 5 specific services I can provide
            - process_items: Array of 4 implementation phases with "title" and "description"
            - unique_value: Why I'm the perfect fit (2-3 sentences)
            - custom_approach: My specific approach to their problem (2-3 sentences)
            
            Focus on automation, integration, and efficiency. Be specific to their needs.
            """

            # Use NEW OpenAI v1.0+ API format
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert automation consultant specializing in Make.com, n8n, Zapier, and API integrations. You analyze client needs and create compelling, specific proposals that demonstrate deep understanding of their challenges. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse AI response using new format
            ai_content = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                import json as json_module
                data = json_module.loads(ai_content)
                return data
            except:
                # If not valid JSON, extract key information intelligently
                return self.parse_ai_text_response_enhanced(ai_content, job)
                
        except Exception as e:
            print(f"AI analysis error: {e}")
            # Fall back to enhanced analysis
            return self.get_enhanced_fallback_content(job)
    
    def get_enhanced_fallback_content(self, job):
        """Enhanced fallback content when AI is unavailable"""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        text = title + ' ' + description
        
        # Intelligent current process detection
        current_process = 'manual workflow management'
        if any(term in text for term in ['excel', 'spreadsheet', 'sheets']):
            current_process = 'spreadsheet-based data management'
        elif any(term in text for term in ['email', 'outlook', 'gmail']):
            current_process = 'email-based communication workflows'
        elif any(term in text for term in ['crm', 'salesforce', 'hubspot']):
            current_process = 'manual CRM data entry'
        elif any(term in text for term in ['inventory', 'stock', 'warehouse']):
            current_process = 'manual inventory tracking'
        elif any(term in text for term in ['leads', 'prospect', 'sales']):
            current_process = 'manual lead qualification'
        
        # Intelligent desired outcome
        desired_outcome = 'streamlined automated workflows'
        if 'save time' in text or 'faster' in text:
            desired_outcome = 'significant time savings and efficiency gains'
        elif 'reduce error' in text or 'accuracy' in text:
            desired_outcome = 'error-free automated operations'
        elif 'scale' in text or 'grow' in text:
            desired_outcome = 'scalable business growth through automation'
        elif 'integrate' in text:
            desired_outcome = 'seamless system integration'
        
        # Smart tool detection
        tools = []
        tool_mapping = {
            'zapier': 'Zapier',
            'n8n': 'n8n', 
            'make.com': 'Make.com',
            'integromat': 'Make.com',
            'airtable': 'Airtable',
            'google sheets': 'Google Sheets',
            'slack': 'Slack',
            'trello': 'Trello',
            'asana': 'Asana',
            'monday': 'Monday.com',
            'hubspot': 'HubSpot',
            'salesforce': 'Salesforce'
        }
        
        for keyword, tool_name in tool_mapping.items():
            if keyword in text and tool_name not in tools:
                tools.append(tool_name)
        
        if not tools:
            # Default based on job type
            if any(term in text for term in ['crm', 'sales', 'lead']):
                tools = ['Make.com', 'HubSpot API', 'Zapier']
            elif any(term in text for term in ['email', 'communication']):
                tools = ['n8n', 'Gmail API', 'Slack']
            else:
                tools = ['Make.com', 'n8n', 'API integrations']
        
        # Context-aware workflow steps
        if 'crm' in text:
            workflow_steps = [
                {'title': 'Lead Capture', 'description': 'Automated lead collection from multiple sources'},
                {'title': 'Data Enrichment', 'description': 'Enhance lead data with additional contact information'},
                {'title': 'CRM Integration', 'description': 'Seamless sync with your CRM system'},
                {'title': 'Follow-up Automation', 'description': 'Automated nurture sequences and notifications'}
            ]
        elif 'email' in text:
            workflow_steps = [
                {'title': 'Email Processing', 'description': 'Intelligent email parsing and categorization'},
                {'title': 'Data Extraction', 'description': 'Extract relevant information from emails'},
                {'title': 'System Updates', 'description': 'Update relevant systems with extracted data'},
                {'title': 'Response Automation', 'description': 'Generate and send appropriate responses'}
            ]
        else:
            workflow_steps = [
                {'title': 'Data Collection', 'description': 'Automated data gathering from multiple sources'},
                {'title': 'Processing & Validation', 'description': 'Intelligent data transformation and validation'},
                {'title': 'System Integration', 'description': 'Seamless connection between all platforms'},
                {'title': 'Automated Actions', 'description': 'Trigger appropriate actions based on processed data'}
            ]
        
        return {
            'current_process': current_process,
            'desired_outcome': desired_outcome,
            'tools': ', '.join(tools),
            'workflow_steps': workflow_steps,
            'services': [
                'Requirements Analysis & Planning',
                'Custom Workflow Development',
                'API Integration & Webhooks',
                'Testing & Quality Assurance',
                'Documentation & Training'
            ],
            'process_items': [
                {
                    'title': 'Discovery & Strategy',
                    'description': 'Deep dive into your requirements to create the perfect automation blueprint'
                },
                {
                    'title': 'Development & Integration',
                    'description': 'Build robust automation with comprehensive error handling'
                },
                {
                    'title': 'Testing & Optimization',
                    'description': 'Rigorous testing to ensure reliability and peak performance'
                },
                {
                    'title': 'Launch & Support',
                    'description': 'Smooth deployment with comprehensive training and ongoing support'
                }
            ],
            'unique_value': 'With 20+ years of experience and $16M+ in automated operations, I specialize in creating bulletproof automation systems that scale with your business.',
            'custom_approach': f'For your specific {self.extract_job_type(title, description)} needs, I\'ll create a tailored solution that integrates seamlessly with your existing workflow while providing immediate efficiency gains.'
        }
    
    def parse_ai_text_response_enhanced(self, ai_content, job):
        """Enhanced parsing of non-JSON AI responses"""
        # If AI didn't return JSON, fall back to enhanced content
        return self.get_enhanced_fallback_content(job)
    
    def extract_job_type(self, title, description):
        """Enhanced job type extraction"""
        text = (title + ' ' + description).lower()
        
        if any(term in text for term in ['crm', 'customer relationship', 'sales management']):
            return 'CRM automation'
        elif any(term in text for term in ['email', 'newsletter', 'communication']):
            return 'email automation'
        elif any(term in text for term in ['workflow', 'process', 'business automation']):
            return 'workflow automation'
        elif any(term in text for term in ['integration', 'connect', 'sync']):
            return 'systems integration'
        elif any(term in text for term in ['api', 'webhook', 'data transfer']):
            return 'API integration'
        elif any(term in text for term in ['lead', 'prospect', 'generation']):
            return 'lead generation automation'
        elif any(term in text for term in ['inventory', 'stock', 'warehouse']):
            return 'inventory management automation'
        else:
            return 'business automation'
    
    def generate_message(self, client_name, job_type, filename, score, analysis=None):
        """Generate enhanced Upwork message with AI insights"""
        proposal_url = f'https://projekt-ai.net/proposals/{filename}'
        
        # Get custom approach from analysis if available
        custom_approach = ''
        if analysis and 'custom_approach' in analysis:
            custom_approach = f"\n\nSpecifically for your project: {analysis['custom_approach']}"
        
        if score >= 80:
            return f"""Hi {client_name}!

I've analyzed your {job_type} requirements and created a comprehensive solution blueprint specifically for your needs.

🚀 I've prepared a detailed project breakdown with timeline, technical approach, and expected outcomes: {proposal_url}

With 20+ years of automation experience and $16M+ in successful implementations, I specialize in creating robust solutions that scale with your business.{custom_approach}

I'm available to start immediately and can have the initial framework ready within 48 hours.

Best regards,
Tim Poulton
Automation Specialist | projekt-ai.net"""
        
        elif score >= 60:
            return f"""Hi {client_name}!

Your {job_type} project caught my attention. I've created a tailored solution approach: {proposal_url}

I specialize in automation systems and have extensive experience with similar implementations.{custom_approach}

Happy to discuss your requirements and timeline.

Best regards,
Tim Poulton"""
        
        else:
            return f"""Hi {client_name},

I've reviewed your {job_type} needs and prepared a solution overview: {proposal_url}

I'd be happy to help streamline your workflow with the right automation approach.

Best regards,
Tim Poulton"""
    
    def create_default_template(self, template_path):
        """Create a default HTML template if none exists"""
        template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proposal for {{CLIENT_NAME}} - {{JOB_TITLE}}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; border-bottom: 2px solid #007cba; padding-bottom: 20px; }
        .section { margin: 30px 0; }
        .workflow-step { display: flex; align-items: center; margin: 15px 0; }
        .step-number { background: #007cba; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; }
        .process-item { margin: 20px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #007cba; }
        ul { list-style-type: none; padding: 0; }
        li { padding: 5px 0; border-bottom: 1px solid #eee; }
        .footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Project Proposal</h1>
            <h2>{{JOB_TITLE}}</h2>
            <p><strong>For:</strong> {{CLIENT_NAME}} | <strong>Budget:</strong> {{JOB_BUDGET}} | <strong>Score:</strong> {{SCORE}}</p>
        </div>
        
        <div class="section">
            <h3>Current Situation</h3>
            <p>{{CURRENT_PROCESS}}</p>
            
            <h3>Desired Outcome</h3>
            <p>{{DESIRED_OUTCOME}}</p>
            
            <h3>Tools & Technologies</h3>
            <p>{{TOOLS}}</p>
        </div>
        
        <div class="section">
            <h3>Workflow Process</h3>
            {{WORKFLOW_STEPS}}
        </div>
        
        <div class="section">
            <h3>Services Included</h3>
            <ul>{{SERVICES}}</ul>
        </div>
        
        <div class="section">
            <h3>Implementation Process</h3>
            {{PROCESS_ITEMS}}
        </div>
        
        <div class="section">
            <h3>Why Choose Me</h3>
            <p>{{UNIQUE_VALUE}}</p>
            
            <h3>Custom Approach</h3>
            <p>{{CUSTOM_APPROACH}}</p>
        </div>
        
        <div class="footer">
            <p>Generated: {{TIMESTAMP}}</p>
            <p><strong>Tim Poulton</strong> | Automation Specialist | projekt-ai.net</p>
        </div>
    </div>
</body>
</html>'''
        
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        with open(template_path, 'w') as f:
            f.write(template_content)
    
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
                
        except Exception as e:
            print(f"Error saving to queue: {e}")

def run_server():
    """Start the proposal server"""
    PORT = 8090
    
    print(f"🚀 Upwork Proposal Server (FIXED) running on port {PORT}")
    print(f"📡 Webhook URL: http://192.168.1.107:{PORT}/webhook/rss-jobs")
    print(f"📝 Proposals saved to: /srv/apps/client-proposals/public/")
    print(f"📋 Review queue: {os.path.join(os.path.dirname(__file__), 'proposal-queue.json')}")
    print("✅ Ready to receive jobs from Upwork scraper!")
    
    with socketserver.TCPServer(("", PORT), UpworkProposalServer) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run_server() 