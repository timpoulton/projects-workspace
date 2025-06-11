#!/usr/bin/env python3
"""
Enhanced Proposal Queue Viewer
Shows proposals organized by priority with detailed scoring information
"""

import json
import os
from datetime import datetime

def view_proposals():
    """View proposals organized by priority"""
    queue_file = '/root/homelab-docs/scripts/upwork-automation/proposal-queue.json'
    
    if not os.path.exists(queue_file):
        print("📭 No proposals in queue yet!")
        return
    
    try:
        with open(queue_file, 'r') as f:
            queue = json.load(f)
    except:
        print("⚠️ Error reading queue file")
        return
    
    if not queue:
        print("📭 Queue is empty!")
        return
    
    # Group proposals by priority
    must_apply = []
    should_apply = []
    consider = []
    
    for proposal in queue:
        priority = proposal.get('priority', 'consider')
        if priority == 'must_apply':
            must_apply.append(proposal)
        elif priority == 'should_apply':
            should_apply.append(proposal)
        else:
            consider.append(proposal)
    
    # Sort each group by score (highest first)
    must_apply.sort(key=lambda x: x.get('score', 0), reverse=True)
    should_apply.sort(key=lambda x: x.get('score', 0), reverse=True)
    consider.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    print(f"\n📊 PROPOSAL QUEUE SUMMARY")
    print(f"{'='*60}")
    print(f"Total proposals: {len(queue)}")
    print(f"  🔴 Must Apply: {len(must_apply)}")
    print(f"  🟡 Should Apply: {len(should_apply)}")
    print(f"  🟢 Consider: {len(consider)}")
    
    # Display each priority group
    if must_apply:
        print(f"\n🔴 MUST APPLY (Score 80+)")
        print(f"{'-'*60}")
        for i, proposal in enumerate(must_apply[:5], 1):  # Show top 5
            display_proposal(i, proposal)
    
    if should_apply:
        print(f"\n🟡 SHOULD APPLY (Score 60-79)")
        print(f"{'-'*60}")
        for i, proposal in enumerate(should_apply[:5], 1):
            display_proposal(i, proposal)
    
    if consider:
        print(f"\n🟢 CONSIDER (Score 40-59)")
        print(f"{'-'*60}")
        for i, proposal in enumerate(consider[:5], 1):
            display_proposal(i, proposal)
    
    # Show action commands
    print(f"\n📋 ACTIONS")
    print(f"{'-'*60}")
    print("View proposals online:")
    print("  https://projekt-ai.net/proposals/")
    print("\nClear queue:")
    print("  rm /root/homelab-docs/scripts/upwork-automation/proposal-queue.json")
    print("\nEdit scoring config:")
    print("  nano /root/homelab-docs/scripts/upwork-automation/scoring-config.json")

def display_proposal(num, proposal):
    """Display a single proposal with key details"""
    job = proposal.get('job', {})
    client = job.get('client', {})
    
    print(f"\n{num}. {job.get('title', 'Unknown')[:60]}...")
    print(f"   Score: {proposal.get('score', 0)} | Budget: {job.get('budget', 'Not specified')}")
    print(f"   Client: ${client.get('totalSpent', 0):,} spent | "
          f"{client.get('location', {}).get('country', 'Unknown')} | "
          f"Verified: {'✓' if client.get('paymentVerified') else '✗'}")
    print(f"   Posted: {format_time(job.get('postedTime', ''))} | "
          f"Proposals: {job.get('proposalsCount', 0)}")
    print(f"   📄 {proposal.get('filename', 'proposal.html')}")

def format_time(posted_time):
    """Format posted time to relative format"""
    if not posted_time:
        return "Unknown"
    
    try:
        if isinstance(posted_time, str):
            posted_dt = datetime.fromisoformat(posted_time.replace('Z', '+00:00'))
        else:
            posted_dt = datetime.fromtimestamp(posted_time / 1000)
        
        now = datetime.now()
        diff = now - posted_dt
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        else:
            return f"{diff.seconds // 60}m ago"
    except:
        return "Unknown"

if __name__ == "__main__":
    view_proposals() 