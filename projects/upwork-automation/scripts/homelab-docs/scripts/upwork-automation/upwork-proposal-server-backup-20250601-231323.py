#!/usr/bin/env python3
"""
Upwork Proposal Automation Server
A simple, all-in-one solution for generating HTML proposals from Upwork jobs
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
import openai

# Configure OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY', '')  # Set via environment variable

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
        client = job.get('client', {})
        client_rules = rules.get('client_quality', {})
        
        # Payment verified
        if client.get('paymentVerified') and client_rules.get('payment_verified', {}).get('points'):
            points = client_rules['payment_verified']['points']
            score += points
            score_breakdown.append(f"Payment verified: +{points}")
        
        # Client spending
        total_spent = client.get('totalSpent', 0)
        for tier in client_rules.get('spending_tiers', []):
            if total_spent >= tier['min']:
                score += tier['points']
                score_breakdown.append(f"{tier['label']}: +{tier['points']}")
                break
        
        # Hire rate
        jobs_posted = client.get('totalJobsPosted', 1)
        hires = client.get('totalHires', 0)
        if jobs_posted > 0:
            hire_rate = (hires / jobs_posted) * 100
            if hire_rate >= client_rules.get('hire_rate', {}).get('min_percentage', 80):
                points = client_rules['hire_rate']['points']
                score += points
                score_breakdown.append(f"Hire rate {hire_rate:.0f}%: +{points}")
        
        # Average rating
        avg_rating = client.get('avgHourlyRate', 0)
        if avg_rating >= client_rules.get('average_rating', {}).get('min_rating', 4.8):
            points = client_rules['average_rating']['points']
            score += points
            score_breakdown.append(f"Client rating {avg_rating}: +{points}")
        
        # Location
        location = client.get('location', {}).get('country', '')
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
        
        # Time posted
        posted_time = job.get('postedTime')
        if posted_time:
            try:
                # Parse the posted time
                if isinstance(posted_time, str):
                    posted_dt = datetime.fromisoformat(posted_time.replace('Z', '+00:00'))
                else:
                    posted_dt = datetime.fromtimestamp(posted_time / 1000)  # If milliseconds
                
                hours_ago = (datetime.now() - posted_dt).total_seconds() / 3600
                
                for time_config in competition_rules.get('time_posted', {}).get('within_hours', []):
                    if hours_ago <= time_config['max']:
                        score += time_config['points']
                        score_breakdown.append(f"{time_config['label']}: +{time_config['points']}")
                        break
            except:
                pass
        
        # 6. Project length
        duration = job.get('duration', '').lower()
        for pref in rules.get('project_length', {}).get('preferences', []):
            if pref['duration'].lower() in duration:
                score += pref['points']
                score_breakdown.append(f"Project length {pref['duration']}: +{pref['points']}")
                break
        
        # Print score breakdown for debugging
        if score_breakdown:
            print(f"\n📊 Score breakdown for '{job.get('title', 'Unknown')[:50]}...':")
            for item in score_breakdown:
                print(f"  • {item}")
            print(f"  📈 Total Score: {score}")
        
        return score
    
    def extract_budget(self, job):
        """Extract numeric budget from various formats"""
        budget_str = str(job.get('budget', ''))
        
        # Remove commas and extract numbers
        matches = re.findall(r'\d+', budget_str.replace(',', ''))
        if matches:
            return int(matches[0])
        
        return 0
    
    def calculate_job_score_basic(self, job):
        """Basic scoring when no config available (fallback)"""
        score = 0
        
        # Budget scoring
        budget = job.get('budget', 0)
        if isinstance(budget, str):
            # Extract number from string like "$2,500"
            matches = re.findall(r'\d+', budget.replace(',', ''))
            budget = int(matches[0]) if matches else 0
        
        if budget >= 5000:
            score += 30
        elif budget >= 2000:
            score += 25
        elif budget >= 1000:
            score += 20
        elif budget >= 500:
            score += 10
        elif 'hourly' in str(job.get('budget', '')).lower():
            score += 15
        
        # Keyword scoring
        description = (job.get('title', '') + ' ' + job.get('description', '')).lower()
        
        high_value_keywords = ['automation', 'workflow', 'integration', 'api', 'webhook']
        for keyword in high_value_keywords:
            if keyword in description:
                score += 10
        
        tool_keywords = ['n8n', 'zapier', 'make.com', 'integromat', 'airtable']
        for tool in tool_keywords:
            if tool in description:
                score += 8
        
        industry_terms = ['crm', 'email', 'database', 'sync', 'connect']
        for term in industry_terms:
            if term in description:
                score += 5
        
        # Client quality
        client = job.get('client', {})
        if client.get('paymentVerified'):
            score += 10
        if client.get('totalSpent', 0) > 10000:
            score += 10
        elif client.get('totalSpent', 0) > 1000:
            score += 5
        
        return score
    
    def generate_proposal(self, job, score):
        """Generate the proposal HTML"""
        title = job.get('title', 'Unknown Job')
        
        # Load template
        template_path = '/root/homelab-docs/projekt-ai-website/templates/dark-proposal-template.html'
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Add score to job object for AI analysis
        job_with_score = dict(job)
        job_with_score['score'] = score
        
        # Analyze job
        description = job.get('description', '')
        analysis = self.analyze_job_with_ai(job_with_score)
        
        # Extract client name
        client_name = 'Your Company'
        if ' for ' in title:
            client_name = title.split(' for ')[-1].strip()
        elif ' - ' in title:
            client_name = title.split(' - ')[-1].strip()
        
        # Calculate metrics based on score
        time_saved = '85' if score >= 70 else '75' if score >= 40 else '65'
        efficiency = '400' if score >= 70 else '300' if score >= 40 else '200'
        
        # Determine timeline and price
        budget = job.get('budget', 0)
        if isinstance(budget, str):
            matches = re.findall(r'\d+', budget.replace(',', ''))
            budget = int(matches[0]) if matches else 1500
        
        timeline = '3-4 weeks' if budget > 3000 else '2-3 weeks'
        price_range = '$3,000-$6,000' if budget > 5000 else '$1,500-$3,000' if budget > 1500 else '$800-$1,500'
        
        # Extract job type
        job_type = self.extract_job_type(title, description)
        
        # Generate workflow steps
        steps = analysis.get('workflow_steps', [
            {
                'title': 'Discovery & Analysis',
                'description': 'Deep dive into your current processes to identify automation opportunities',
                'icon': '🔍'
            },
            {
                'title': 'Workflow Design',
                'description': 'Create custom automation blueprint tailored to your specific needs',
                'icon': '📐'
            },
            {
                'title': 'Development & Integration',
                'description': 'Build and connect all systems with robust error handling',
                'icon': '⚡'
            },
            {
                'title': 'Testing & Optimization',
                'description': 'Thoroughly test all scenarios and optimize for performance',
                'icon': '✅'
            }
        ])
        
        # Services based on AI analysis
        services = analysis.get('services', [
            'Requirements Analysis',
            'Custom Workflow Development',
            f'{analysis.get("tools", "API")} Integration',
            'Error Handling & Monitoring',
            'Documentation & Training'
        ])
        
        # Process items from AI
        process_items = analysis.get('process_items', [
            {
                'title': 'Discovery & Mapping',
                'desc': 'We\'ll analyze your current workflow to identify automation opportunities and create a detailed implementation roadmap'
            },
            {
                'title': 'Integration Setup',
                'desc': f'Connect {analysis.get("tools", "your systems")} with secure authentication and configure all necessary permissions and data flows'
            },
            {
                'title': 'Workflow Development',
                'desc': 'Build custom automation logic with error handling, data validation, and performance optimization'
            },
            {
                'title': 'Launch & Support',
                'desc': 'Deploy your automation with comprehensive testing, team training, and 30 days of dedicated support'
            }
        ])
        
        # Use AI-generated unique value proposition
        unique_value = analysis.get('unique_value', '')
        custom_approach = analysis.get('custom_approach', '')
        
        # Enhanced subtitle with AI insights
        project_subtitle = f'Transform your {analysis.get("current_process", "manual processes")} into an intelligent automation system that delivers {analysis.get("desired_outcome", "exceptional results")}. {unique_value}'
        
        # Replace placeholders
        replacements = {
            '[CLIENT_NAME]': client_name,
            '[PROJECT_TYPE]': job_type.title(),
            '[PROJECT_TITLE]': f'{job_type.title()} Solution',
            '[PROJECT_SUBTITLE]': project_subtitle,
            '[CURRENT_PROCESS]': analysis.get('current_process', 'manual processes'),
            '[DESIRED_OUTCOME]': analysis.get('desired_outcome', 'streamlined automation'),
            '[PRICE_RANGE]': price_range,
            '[DELIVERY_WEEKS]': timeline,
            '[WORKFLOW_SUBTITLE]': f'Automated {job_type} from start to finish'
        }
        
        # Add service replacements
        for i, service in enumerate(services, 1):
            replacements[f'[SERVICE_{i}]'] = service
        
        # Add workflow step replacements
        for i, step in enumerate(steps, 1):
            replacements[f'[STEP_{i}_ICON]'] = step['icon']
            replacements[f'[STEP_{i}_TITLE]'] = step['title']
            replacements[f'[STEP_{i}_DESC]'] = step['description'][:50] + '...' if len(step['description']) > 50 else step['description']
        
        # Add process replacements
        for i, process in enumerate(process_items, 1):
            replacements[f'[PROCESS_{i}_TITLE]'] = process['title']
            replacements[f'[PROCESS_{i}_DESC]'] = process['desc']
        
        # Add stats replacements
        replacements['[STAT_1_VALUE]'] = time_saved
        replacements['[STAT_1_LABEL]'] = 'Time Saved'
        replacements['[STAT_2_VALUE]'] = '99'
        replacements['[STAT_2_LABEL]'] = 'Accuracy'
        replacements['[STAT_3_VALUE]'] = efficiency
        replacements['[STAT_3_LABEL]'] = 'Efficiency Gain'
        
        # Apply replacements
        proposal_html = template
        for placeholder, value in replacements.items():
            proposal_html = proposal_html.replace(placeholder, value)
        
        # Generate filename
        timestamp = int(time.time() * 1000)
        safe_name = re.sub(r'[^a-z0-9]+', '-', client_name.lower())
        filename = f'{safe_name}-proposal-{timestamp}.html'
        
        # Save proposal to web directory
        proposals_dir = '/srv/apps/client-proposals/public/'
        os.makedirs(proposals_dir, exist_ok=True)
        filepath = os.path.join(proposals_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(proposal_html)
        
        # Set proper permissions
        os.chmod(filepath, 0o644)
        
        # Generate Upwork message
        message = self.generate_message(client_name, job_type, filename, score, analysis)
        
        return {
            'job_id': job.get('url', '').split('/')[-1],
            'job_title': title,
            'client_name': client_name,
            'score': score,
            'proposal_url': f'https://projekt-ai.net/proposals/{filename}',
            'message': message,
            'filename': filename,
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_job_with_ai(self, job):
        """Use OpenAI to analyze job and generate custom content"""
        if not openai.api_key:
            return self.get_default_ai_content()
        
        try:
            # Determine AI depth based on score
            score = job.get('score', 0)
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
            - tools: List of tools/platforms mentioned or that would be useful
            - workflow_steps: Array of 4 steps, each with "icon" and "text" fields
            - services: Array of 5 specific services I can provide
            - process_items: Array of 4 implementation phases with "phase" and "description"
            - unique_value: Why I'm the perfect fit (2-3 sentences)
            - custom_approach: My specific approach to their problem (2-3 sentences)
            
            Focus on automation, integration, and efficiency. Be specific to their needs.
            """

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert automation consultant specializing in Make.com, n8n, Zapier, and API integrations. You analyze client needs and create compelling, specific proposals that demonstrate deep understanding of their challenges."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse AI response
            ai_content = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                import json as json_module
                data = json_module.loads(ai_content)
                return data
            except:
                # If not valid JSON, extract key information
                return self.parse_ai_text_response(ai_content, job.get('description', ''), job.get('title', ''))
                
        except Exception as e:
            print(f"AI analysis error: {e}")
            # Fall back to basic analysis
            return self.analyze_job_basic(job.get('description', ''), job.get('title', ''))
    
    def parse_ai_text_response(self, ai_content, description, title):
        """Parse non-JSON AI response into structured data"""
        # Extract information from text response
        # This is a fallback if AI doesn't return proper JSON
        return {
            'current_process': 'manual workflow management',
            'desired_outcome': 'automated and streamlined operations',
            'tools': 'Make.com, n8n, API integrations',
            'workflow_steps': [
                {'title': 'Data Collection', 'description': 'Automated data gathering from multiple sources', 'icon': '📊'},
                {'title': 'Processing', 'description': 'Intelligent data transformation and validation', 'icon': '⚙️'},
                {'title': 'Integration', 'description': 'Seamless connection between all systems', 'icon': '🔗'},
                {'title': 'Delivery', 'description': 'Automated output and reporting', 'icon': '🚀'}
            ],
            'services': [
                'Requirements Analysis',
                'Custom Workflow Development', 
                'API Integration',
                'Testing & Optimization',
                'Documentation & Training'
            ],
            'process_items': [
                {
                    'title': 'Discovery & Planning',
                    'desc': 'Deep dive into your requirements to create the perfect automation strategy'
                },
                {
                    'title': 'Development & Integration',
                    'desc': 'Build robust automation with error handling and performance optimization'
                },
                {
                    'title': 'Testing & Refinement',
                    'desc': 'Comprehensive testing to ensure reliability and efficiency'
                },
                {
                    'title': 'Launch & Support',
                    'desc': 'Smooth deployment with training and ongoing support'
                }
            ],
            'unique_value': ai_content[:200] if ai_content else 'Proven expertise in similar automation projects',
            'custom_approach': 'Tailored solution designed specifically for your workflow'
        }
    
    def analyze_job_basic(self, description, title):
        """Basic pattern matching analysis (fallback when no AI)"""
        # Current process
        current_process = 'manual data management'
        if 'excel' in description or 'spreadsheet' in description:
            current_process = 'spreadsheet-based tracking'
        elif 'email' in description:
            current_process = 'email-based workflows'
        elif 'paper' in description or 'manual' in description:
            current_process = 'manual processes'
        
        # Desired outcome
        desired_outcome = 'streamlined automation'
        if 'save time' in description:
            desired_outcome = 'significant time savings'
        elif 'reduce error' in description:
            desired_outcome = 'error-free operations'
        elif 'scale' in description:
            desired_outcome = 'scalable growth'
        
        # Tools
        tools = []
        tool_map = {
            'zapier': 'Zapier',
            'n8n': 'n8n',
            'make.com': 'Make.com',
            'integromat': 'Make.com',
            'airtable': 'Airtable',
            'google sheets': 'Google Sheets',
            'slack': 'Slack'
        }
        
        for keyword, tool_name in tool_map.items():
            if keyword in description:
                tools.append(tool_name)
        
        if not tools:
            tools = ['n8n', 'API integrations', 'Custom webhooks']
        
        return {
            'current_process': current_process,
            'desired_outcome': desired_outcome,
            'tools': ', '.join(tools)
        }
    
    def extract_job_type(self, title, description):
        """Extract the type of automation needed"""
        text = (title + ' ' + description).lower()
        
        if 'crm' in text:
            return 'CRM automation'
        elif 'email' in text:
            return 'email automation'
        elif 'workflow' in text:
            return 'workflow automation'
        elif 'integration' in text:
            return 'systems integration'
        elif 'api' in text:
            return 'API integration'
        else:
            return 'automation'
    
    def generate_message(self, client_name, job_type, filename, score, analysis=None):
        """Generate Upwork message with AI insights"""
        proposal_url = f'https://projekt-ai.net/proposals/{filename}'
        
        # Get custom approach from AI analysis if available
        custom_approach = ''
        if analysis and 'custom_approach' in analysis:
            custom_approach = f"\n\nSpecifically for your project: {analysis['custom_approach']}"
        
        if score >= 70:
            return f"""Hi there!

I noticed you need help with {job_type}. I've actually created a custom automation workflow and project breakdown specifically for your requirements.

You can view your personalized proposal here:
→ {proposal_url}

This demonstrates exactly how I'd solve your specific challenges, including the tools, timeline, and investment required.{custom_approach}

I'm particularly excited about this project because it aligns perfectly with my expertise in building similar systems.

Looking forward to discussing this with you!

Best regards,
Tim"""
        elif score >= 40:
            return f"""Hi!

I specialize in {job_type} and would love to help with your project.

I've prepared a detailed proposal showing how I'd approach your specific needs:
→ {proposal_url}

The proposal includes my recommended workflow, timeline, and pricing.

Let me know if you'd like to discuss further!

Best,
Tim"""
        else:
            return f"""Hello,

I can help with your {job_type} project.

Here's my proposal with details on approach and pricing:
→ {proposal_url}

Happy to answer any questions!

Tim"""
    
    def save_to_queue(self, proposal_data):
        """Save proposal to review queue"""
        queue_file = '/root/homelab-docs/scripts/upwork-automation/proposal-queue.json'
        
        # Load existing queue
        queue = []
        if os.path.exists(queue_file):
            with open(queue_file, 'r') as f:
                queue = json.load(f)
        
        # Add new proposal
        queue.append(proposal_data)
        
        # Keep only last 100 proposals
        queue = queue[-100:]
        
        # Save updated queue
        os.makedirs(os.path.dirname(queue_file), exist_ok=True)
        with open(queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        
        print(f"✅ Saved to queue: {proposal_data['client_name']} (Score: {proposal_data['score']})")

def run_server():
    """Run the webhook server"""
    PORT = 8090
    Handler = UpworkProposalServer
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Upwork Proposal Server running on port {PORT}")
        print(f"📡 Webhook URL: http://192.168.1.107:{PORT}/webhook/rss-jobs")
        print(f"📝 Proposals saved to: /srv/apps/client-proposals/public/")
        print(f"📋 Review queue: /root/homelab-docs/scripts/upwork-automation/proposal-queue.json")
        print(f"\n✅ Ready to receive jobs from Upwork scraper!")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server() 