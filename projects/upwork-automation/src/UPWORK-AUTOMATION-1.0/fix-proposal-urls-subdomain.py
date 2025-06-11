#!/usr/bin/env python3
"""
Fix Proposal URLs to use correct subdomain
Updates all proposal URLs from projekt-ai.net/proposals/ to proposals.projekt-ai.net/
"""

import json
import os

QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"

def fix_proposal_urls():
    """Fix proposal URLs to use correct subdomain"""
    
    print("🔧 FIXING PROPOSAL URLS TO USE CORRECT SUBDOMAIN")
    print("📋 Updating from projekt-ai.net/proposals/ to proposals.projekt-ai.net/")
    print()
    
    # Load current queue
    with open(QUEUE_FILE, 'r') as f:
        proposals = json.load(f)
    
    print(f"Found {len(proposals)} proposals to check")
    
    fixed_count = 0
    
    for proposal in proposals:
        current_url = proposal.get('proposal_url', '')
        
        # Check if URL needs fixing
        if 'projekt-ai.net/proposals/' in current_url:
            # Extract filename from the URL
            filename = current_url.split('/')[-1]
            
            # Generate correct URL with subdomain
            correct_url = f"https://proposals.projekt-ai.net/{filename}"
            
            print(f"✅ Fixing: {proposal.get('job_title', 'Unknown')[:50]}...")
            print(f"   Old: {current_url}")
            print(f"   New: {correct_url}")
            
            proposal['proposal_url'] = correct_url
            fixed_count += 1
    
    # Save updated queue
    with open(QUEUE_FILE, 'w') as f:
        json.dump(proposals, f, indent=2)
    
    # Also sync to web directory
    web_queue = "/srv/apps/client-proposals/public/proposal-queue.json"
    os.makedirs(os.path.dirname(web_queue), exist_ok=True)
    with open(web_queue, 'w') as f:
        json.dump(proposals, f, indent=2)
    
    print(f"\n🎯 FIXED {fixed_count} PROPOSAL URLS")
    print(f"📝 Updated queue saved to {QUEUE_FILE}")
    print(f"🌐 Updated web queue saved to {web_queue}")
    print(f"✨ All proposals now use: https://proposals.projekt-ai.net/")

if __name__ == "__main__":
    fix_proposal_urls() 