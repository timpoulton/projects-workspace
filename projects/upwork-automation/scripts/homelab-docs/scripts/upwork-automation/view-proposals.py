#!/usr/bin/env python3
"""
View and manage Upwork proposal queue
"""

import json
import os
import sys
from datetime import datetime

def view_queue():
    """Display all proposals in the queue"""
    queue_file = '/root/homelab-docs/scripts/upwork-automation/proposal-queue.json'
    
    if not os.path.exists(queue_file):
        print("❌ No proposals in queue yet")
        return
    
    with open(queue_file, 'r') as f:
        queue = json.load(f)
    
    if not queue:
        print("❌ Queue is empty")
        return
    
    print(f"\n📋 Proposal Queue ({len(queue)} items)\n")
    print("-" * 80)
    
    for i, proposal in enumerate(queue[-10:], 1):  # Show last 10
        print(f"\n{i}. {proposal['client_name']} - Score: {proposal['score']}")
        print(f"   Job: {proposal['job_title']}")
        print(f"   URL: {proposal['proposal_url']}")
        print(f"   Time: {proposal['timestamp']}")
        print(f"\n   Message Preview:")
        print("   " + proposal['message'].split('\n')[0][:60] + "...")
        print("-" * 80)

def show_message(index):
    """Show full message for a specific proposal"""
    queue_file = '/root/homelab-docs/scripts/upwork-automation/proposal-queue.json'
    
    with open(queue_file, 'r') as f:
        queue = json.load(f)
    
    try:
        proposal = queue[-index]  # Negative index from end
        print(f"\n📝 Full Message for: {proposal['client_name']}")
        print("=" * 80)
        print(proposal['message'])
        print("=" * 80)
        print(f"\n🔗 Proposal URL: {proposal['proposal_url']}")
        print(f"📋 Copy this message to Upwork!\n")
    except IndexError:
        print("❌ Invalid index")

def clear_queue():
    """Clear the proposal queue"""
    queue_file = '/root/homelab-docs/scripts/upwork-automation/proposal-queue.json'
    
    if input("Are you sure you want to clear the queue? (y/n): ").lower() == 'y':
        with open(queue_file, 'w') as f:
            json.dump([], f)
        print("✅ Queue cleared")
    else:
        print("❌ Cancelled")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "clear":
            clear_queue()
        elif sys.argv[1] == "show" and len(sys.argv) > 2:
            show_message(int(sys.argv[2]))
        else:
            print("Usage: view-proposals.py [clear | show <number>]")
    else:
        view_queue() 