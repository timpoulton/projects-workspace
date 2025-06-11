#!/usr/bin/env python3
"""
Add Missing Filenames to Proposals
Adds filename field to proposals that are missing it
"""

import json
import time

QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"

def generate_filename_from_url(proposal_url):
    """Extract filename from proposal URL"""
    if proposal_url:
        return proposal_url.split('/')[-1]
    return None

def generate_filename_from_title(job_title, timestamp_str):
    """Generate filename from job title and timestamp"""
    # Clean title
    safe_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_'))
    safe_title = safe_title.replace(' ', '-')[:50]
    
    # Extract timestamp from created_at or use current time
    try:
        # Try to extract timestamp from created_at
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        timestamp = int(dt.timestamp() * 1000)
    except:
        timestamp = int(time.time() * 1000)
    
    return f"proposal-{safe_title}-{timestamp}.html"

def add_missing_filenames():
    """Add missing filenames to proposals"""
    
    print("🔧 ADDING MISSING FILENAMES TO PROPOSALS")
    print()
    
    # Load proposals from queue
    with open(QUEUE_FILE, 'r') as f:
        proposals = json.load(f)
    
    print(f"Found {len(proposals)} proposals in queue")
    
    updated_count = 0
    
    for proposal in proposals:
        if 'filename' not in proposal or not proposal['filename']:
            job_title = proposal.get('job_title', 'Unknown')
            
            # Try to get filename from URL first
            filename = generate_filename_from_url(proposal.get('proposal_url', ''))
            
            # If that fails, generate from title and timestamp
            if not filename:
                filename = generate_filename_from_title(
                    job_title, 
                    proposal.get('created_at', '')
                )
            
            proposal['filename'] = filename
            print(f"✅ Added filename: {job_title[:50]}... -> {filename}")
            updated_count += 1
        else:
            print(f"✅ Already has filename: {proposal.get('job_title', 'Unknown')[:50]}...")
    
    # Save updated queue
    with open(QUEUE_FILE, 'w') as f:
        json.dump(proposals, f, indent=2)
    
    # Also sync to web directory
    web_queue = "/srv/apps/client-proposals/public/proposal-queue.json"
    with open(web_queue, 'w') as f:
        json.dump(proposals, f, indent=2)
    
    print(f"\n🎯 ADDED FILENAMES TO {updated_count} PROPOSALS")
    print(f"📝 Updated queue saved to {QUEUE_FILE}")
    print(f"🌐 Updated web queue saved to {web_queue}")

if __name__ == "__main__":
    add_missing_filenames() 