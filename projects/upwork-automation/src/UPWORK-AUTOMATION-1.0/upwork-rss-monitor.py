#!/usr/bin/env python3
"""
Upwork Proposal Automation - RSS Monitor
Implements the proven $500k+ freelancer methodology for systematic business development.

Based on analysis from successful automation freelancers:
- 80% pre-templated content + 20% AI-generated variables
- Meta-automation approach: automation demonstrates automation capability
- Multi-asset coordination: proposal + doc + workflow diagram
"""

import feedparser
import requests
import json
import time
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

class UpworkRSSMonitor:
    """
    RSS-driven market intelligence system for Upwork automation projects
    """
    
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.processed_jobs_file = "processed_jobs.json"
        self.processed_jobs = self.load_processed_jobs()
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration or create default"""
        default_config = {
            "rss_feeds": [
                "https://www.upwork.com/ab/feed/jobs/rss?q=automation&sort=recency",
                "https://www.upwork.com/ab/feed/jobs/rss?q=workflow%20automation&sort=recency",
                "https://www.upwork.com/ab/feed/jobs/rss?q=no%20code&sort=recency",
                "https://www.upwork.com/ab/feed/jobs/rss?q=CRM%20integration&sort=recency",
                "https://www.upwork.com/ab/feed/jobs/rss?q=project%20management%20automation&sort=recency"
            ],
            "target_keywords": [
                "automation", "workflow", "integration", "API", "webhook",
                "zapier", "make.com", "n8n", "no-code", "low-code",
                "CRM", "project management", "business process"
            ],
            "min_budget": 1000,
            "excluded_keywords": [
                "marketing", "social media", "content writing", "SEO",
                "graphic design", "video editing", "translation"
            ],
            "monitoring_interval": 1800,  # 30 minutes
            "max_jobs_per_run": 10
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def load_processed_jobs(self) -> Dict:
        """Load list of already processed jobs"""
        if os.path.exists(self.processed_jobs_file):
            with open(self.processed_jobs_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_processed_jobs(self):
        """Save processed jobs to file"""
        with open(self.processed_jobs_file, 'w') as f:
            json.dump(self.processed_jobs, f, indent=2)
    
    def fetch_jobs_from_feed(self, feed_url: str) -> List[Dict]:
        """Fetch and parse jobs from RSS feed"""
        try:
            print(f"📡 Fetching from: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            jobs = []
            for entry in feed.entries:
                job = {
                    'id': entry.id if hasattr(entry, 'id') else entry.link,
                    'title': entry.title,
                    'description': entry.description if hasattr(entry, 'description') else '',
                    'link': entry.link,
                    'published': entry.published if hasattr(entry, 'published') else '',
                    'source_feed': feed_url
                }
                jobs.append(job)
            
            print(f"✅ Found {len(jobs)} jobs in feed")
            return jobs
            
        except Exception as e:
            print(f"❌ Error fetching feed {feed_url}: {e}")
            return []
    
    def extract_budget(self, description: str) -> Optional[int]:
        """Extract budget from job description"""
        # Common budget patterns in Upwork descriptions
        budget_patterns = [
            r'\$(\d{1,3}(?:,\d{3})*)',  # $1,000 format
            r'(\d{1,3}(?:,\d{3})*)\s*dollars?',  # 1000 dollars
            r'budget[:\s]*\$?(\d{1,3}(?:,\d{3})*)',  # budget: $1000
            r'(\d{1,3}(?:,\d{3})*)\s*USD',  # 1000 USD
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                budget_str = match.group(1).replace(',', '')
                try:
                    return int(budget_str)
                except ValueError:
                    continue
        
        return None
    
    def is_relevant_job(self, job: Dict) -> bool:
        """Check if job matches our targeting criteria"""
        title = job['title'].lower()
        description = job['description'].lower()
        full_text = f"{title} {description}"
        
        # Check for target keywords
        keyword_match = any(keyword.lower() in full_text for keyword in self.config['target_keywords'])
        
        # Check for excluded keywords
        excluded_match = any(keyword.lower() in full_text for keyword in self.config['excluded_keywords'])
        
        # Check budget if extractable
        budget = self.extract_budget(job['description'])
        budget_ok = budget is None or budget >= self.config['min_budget']
        
        # Check if already processed
        already_processed = job['id'] in self.processed_jobs
        
        result = keyword_match and not excluded_match and budget_ok and not already_processed
        
        if result:
            print(f"✅ RELEVANT: {job['title'][:50]}...")
            if budget:
                print(f"   💰 Budget: ${budget:,}")
        else:
            print(f"⏭️  SKIPPED: {job['title'][:50]}...")
            if already_processed:
                print(f"   📋 Already processed")
            elif excluded_match:
                print(f"   🚫 Contains excluded keywords")
            elif not keyword_match:
                print(f"   🎯 No target keywords found")
            elif not budget_ok:
                print(f"   💰 Budget too low: ${budget:,}" if budget else "   💰 Budget not found")
        
        return result
    
    def generate_proposal_assets(self, job: Dict) -> Dict:
        """Generate the three coordinated assets for a job"""
        print(f"🎨 Generating assets for: {job['title']}")
        
        # Asset 1: Proposal text (80% template + 20% AI variables)
        proposal_text = self.generate_proposal_text(job)
        
        # Asset 2: Project breakdown document
        project_doc = self.generate_project_document(job)
        
        # Asset 3: Workflow diagram (Mermaid format)
        workflow_diagram = self.generate_workflow_diagram(job)
        
        assets = {
            'proposal_text': proposal_text,
            'project_document': project_doc,
            'workflow_diagram': workflow_diagram,
            'generated_at': datetime.now().isoformat(),
            'job_info': job
        }
        
        return assets
    
    def generate_proposal_text(self, job: Dict) -> str:
        """Generate proposal text using 80/20 template methodology"""
        
        # Extract key variables from job
        job_type = self.extract_job_type(job)
        client_industry = self.extract_industry(job)
        
        # 80% template structure with 20% AI variables
        template = f"""Hi there!

I do {job_type} automation all the time and I'm really confident I'm the right fit for this project. 

I've actually just done something custom for you - I created a workflow diagram plus a detailed project breakdown for your {job_type} automation in no-code tools.

What makes me different:
• I specialize in {job_type} and have automated similar processes for {client_industry} businesses
• I use proven tools like Make.com, n8n, and Zapier to create reliable, scalable solutions
• I provide complete documentation and training so your team can manage the system

I've attached:
1. Custom workflow diagram showing exactly how I'd automate your process
2. Detailed project document with timeline and deliverables
3. Examples of similar automation projects I've completed

This isn't a template - I spent time understanding your specific needs and created these custom deliverables to show you exactly what I can do.

Ready to turn your manual process into an automated system? Let's discuss the details.

Best regards,
Tim Poulton
Automation Specialist | Projekt AI
"""
        
        return template
    
    def extract_job_type(self, job: Dict) -> str:
        """Extract the type of automation needed from job description"""
        title = job['title'].lower()
        description = job['description'].lower()
        
        if any(word in title + description for word in ['crm', 'customer', 'sales']):
            return "CRM integration"
        elif any(word in title + description for word in ['workflow', 'process', 'approval']):
            return "workflow automation"
        elif any(word in title + description for word in ['email', 'marketing', 'campaign']):
            return "email automation"
        elif any(word in title + description for word in ['data', 'sync', 'integration']):
            return "data integration"
        else:
            return "business process automation"
    
    def extract_industry(self, job: Dict) -> str:
        """Extract likely industry from job description"""
        description = job['description'].lower()
        
        industries = {
            'e-commerce': ['shop', 'store', 'ecommerce', 'retail', 'product'],
            'real estate': ['property', 'real estate', 'realty', 'listings'],
            'healthcare': ['medical', 'health', 'clinic', 'patient'],
            'education': ['school', 'university', 'student', 'course'],
            'finance': ['bank', 'finance', 'investment', 'accounting'],
            'technology': ['software', 'tech', 'development', 'SaaS'],
            'consulting': ['consulting', 'agency', 'service', 'client']
        }
        
        for industry, keywords in industries.items():
            if any(keyword in description for keyword in keywords):
                return industry
        
        return "service-based"
    
    def generate_project_document(self, job: Dict) -> str:
        """Generate detailed project breakdown document"""
        job_type = self.extract_job_type(job)
        
        doc = f"""# {job_type.title()} Project Breakdown
## For: {job['title']}

### Project Overview
This document outlines a comprehensive automation solution for your {job_type} requirements, utilizing proven no-code/low-code tools and methodologies.

### Proposed Solution Architecture

#### Phase 1: Discovery & Planning (Week 1)
- Detailed process mapping of current workflow
- Identification of automation opportunities
- Tool selection and architecture design
- Integration requirements analysis

#### Phase 2: Core Automation Development (Weeks 2-3)
- Primary workflow automation setup
- API integrations and data connections
- Error handling and validation rules
- Initial testing and refinement

#### Phase 3: Enhancement & Optimization (Week 4)
- Advanced features implementation
- Performance optimization
- User interface customization
- Comprehensive testing

#### Phase 4: Documentation & Training (Week 5)
- Complete system documentation
- User training sessions
- Handover and ongoing support setup

### Technical Deliverables
- ✅ Fully automated {job_type} system
- ✅ Custom workflow diagrams and documentation
- ✅ Integration with existing tools
- ✅ User training and support materials
- ✅ 30-day post-launch support

### Investment
Based on the scope and complexity, this project represents significant value through:
- Reduced manual processing time (estimated 80%+ time savings)
- Improved accuracy and consistency
- Scalable foundation for future growth
- Complete documentation for internal management

### Next Steps
1. Schedule discovery call to review requirements
2. Finalize technical specifications
3. Begin development with weekly progress updates
4. Deploy and train your team

This proposal demonstrates our systematic approach and proven methodology for {job_type} automation projects.
"""
        
        return doc
    
    def generate_workflow_diagram(self, job: Dict) -> str:
        """Generate Mermaid workflow diagram"""
        job_type = self.extract_job_type(job)
        
        # Different diagram templates based on job type
        if "crm" in job_type.lower():
            diagram = """
graph LR
    A[New Lead] --> B[Lead Qualification]
    B --> C{Meets Criteria?}
    C -->|Yes| D[Add to CRM]
    C -->|No| E[Nurture Sequence]
    D --> F[Assign Sales Rep]
    F --> G[Send Welcome Email]
    G --> H[Schedule Follow-up]
    E --> I[Educational Content]
    I --> J[Re-qualify Later]
    H --> K[Track Engagement]
    K --> L[Update CRM Status]
"""
        elif "workflow" in job_type.lower():
            diagram = """
graph TD
    A[Process Trigger] --> B[Data Collection]
    B --> C[Validation Check]
    C --> D{Valid Data?}
    D -->|Yes| E[Process Approval]
    D -->|No| F[Error Handling]
    E --> G[Automated Processing]
    F --> B
    G --> H[Update Systems]
    H --> I[Notify Stakeholders]
    I --> J[Archive Results]
"""
        elif "email" in job_type.lower():
            diagram = """
graph LR
    A[Trigger Event] --> B[Audience Selection]
    B --> C[Content Personalization]
    C --> D[Email Generation]
    D --> E[Send Email]
    E --> F[Track Opens/Clicks]
    F --> G{Engagement?}
    G -->|High| H[Follow-up Sequence]
    G -->|Low| I[Re-engagement Campaign]
    H --> J[Update Contact Score]
    I --> J
"""
        else:
            diagram = """
graph TB
    A[Data Input] --> B[Processing Engine]
    B --> C[Business Rules]
    C --> D[Automation Logic]
    D --> E[Output Generation]
    E --> F[System Updates]
    F --> G[Notifications]
    G --> H[Reporting]
"""
        
        return f"```mermaid\n{diagram.strip()}\n```"
    
    def save_assets(self, job_id: str, assets: Dict):
        """Save generated assets to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        job_folder = f"jobs/{job_id}_{timestamp}"
        os.makedirs(job_folder, exist_ok=True)
        
        # Save proposal text
        with open(f"{job_folder}/proposal.txt", 'w') as f:
            f.write(assets['proposal_text'])
        
        # Save project document
        with open(f"{job_folder}/project_breakdown.md", 'w') as f:
            f.write(assets['project_document'])
        
        # Save workflow diagram
        with open(f"{job_folder}/workflow_diagram.md", 'w') as f:
            f.write(assets['workflow_diagram'])
        
        # Save job info and metadata
        with open(f"{job_folder}/job_info.json", 'w') as f:
            json.dump(assets['job_info'], f, indent=2)
        
        print(f"💾 Assets saved to: {job_folder}")
        return job_folder
    
    def monitor_feeds(self):
        """Main monitoring loop"""
        print(f"🎯 Starting Upwork RSS Monitor")
        print(f"⏰ Monitoring {len(self.config['rss_feeds'])} feeds every {self.config['monitoring_interval']/60} minutes")
        
        all_jobs = []
        
        # Fetch from all feeds
        for feed_url in self.config['rss_feeds']:
            jobs = self.fetch_jobs_from_feed(feed_url)
            all_jobs.extend(jobs)
        
        print(f"📊 Total jobs found: {len(all_jobs)}")
        
        # Filter relevant jobs
        relevant_jobs = [job for job in all_jobs if self.is_relevant_job(job)]
        
        print(f"🎯 Relevant jobs: {len(relevant_jobs)}")
        
        # Process top jobs (limit per run)
        jobs_to_process = relevant_jobs[:self.config['max_jobs_per_run']]
        
        for job in jobs_to_process:
            try:
                print(f"\n🔄 Processing: {job['title']}")
                
                # Generate assets
                assets = self.generate_proposal_assets(job)
                
                # Save assets
                job_folder = self.save_assets(job['id'], assets)
                
                # Mark as processed
                self.processed_jobs[job['id']] = {
                    'processed_at': datetime.now().isoformat(),
                    'title': job['title'],
                    'folder': job_folder
                }
                
                print(f"✅ Completed: {job['title']}")
                
            except Exception as e:
                print(f"❌ Error processing job {job['title']}: {e}")
        
        # Save processed jobs list
        self.save_processed_jobs()
        
        print(f"\n🎉 Monitoring cycle complete!")
        print(f"📈 Processed: {len(jobs_to_process)} jobs")
        print(f"💾 Total tracked: {len(self.processed_jobs)} jobs")

def main():
    """Main entry point"""
    monitor = UpworkRSSMonitor()
    
    try:
        monitor.monitor_feeds()
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error in main loop: {e}")

if __name__ == "__main__":
    main() 