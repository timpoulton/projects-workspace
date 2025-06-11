#!/usr/bin/env python3
"""
Fix Proposal URLs Script
Updates the proposal queue to match actual saved files
"""

import json
import os
import glob
import re

QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
PROPOSALS_DIR = "/var/www/projekt-ai.net/proposals/"

def fix_proposal_urls():
    """Fix proposal URLs to match actual saved files"""
    
    # Load current queue
    with open(QUEUE_FILE, 'r') as f:
        proposals = json.load(f)
    
    # Get all actual proposal files
    actual_files = glob.glob(os.path.join(PROPOSALS_DIR, "proposal-*.html"))
    actual_filenames = [os.path.basename(f) for f in actual_files]
    
    print(f"Found {len(actual_filenames)} actual proposal files")
    print(f"Found {len(proposals)} proposals in queue")
    
    fixed_count = 0
    
    for proposal in proposals:
        job_title = proposal.get('job_title', '')
        current_url = proposal.get('proposal_url', '')
        
        if not job_title:
            continue
            
        # Clean job title for matching
        clean_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_'))
        clean_title = clean_title.replace(' ', '-')[:50]
        
        # Find matching file
        pattern = f"proposal-{clean_title}-"
        matching_files = [f for f in actual_filenames if f.startswith(pattern)]
        
        if matching_files:
            # Use the most recent matching file
            matching_file = sorted(matching_files)[-1]
            correct_url = f"https://projekt-ai.net/proposals/{matching_file}"
            
            if current_url != correct_url:
                print(f"Fixing: {job_title}")
                print(f"  Old: {current_url}")
                print(f"  New: {correct_url}")
                proposal['proposal_url'] = correct_url
                proposal['filename'] = matching_file
                fixed_count += 1
    
    # Save updated queue
    with open(QUEUE_FILE, 'w') as f:
        json.dump(proposals, f, indent=2)
    
    print(f"\n✅ Fixed {fixed_count} proposal URLs")
    print(f"📝 Updated queue saved to {QUEUE_FILE}")

if __name__ == "__main__":
    fix_proposal_urls() 