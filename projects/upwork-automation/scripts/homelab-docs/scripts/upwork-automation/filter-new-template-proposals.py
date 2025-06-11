#!/usr/bin/env python3
"""
Filter Proposals by Template Type
Identifies proposals using new dark theme template vs old templates
"""

import json
import os
import glob
from datetime import datetime

# Paths
PROPOSALS_DIR = "/var/www/projekt-ai.net/proposals/"
NETLIFY_PROPOSALS_DIR = "/root/homelab-docs/projekt-ai-website/proposals/"
QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"

def check_template_type(file_path):
    """Check if a proposal file uses the new dark theme template"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # New template indicators
        new_template_indicators = [
            'DARK THEME PROPOSAL - PROJEKT AI DESIGN',
            'Inter:wght@300;400;500;600;700',
            'backdrop-filter: blur(20px)',
            'rgba(26, 26, 26, 0.95)',
            '.workflow-step:hover',
            '.hero-content'
        ]
        
        # Old template indicators
        old_template_indicators = [
            'font-family: \'Inter\', -apple-system, sans-serif; line-height: 1.6; color: #333',
            'background: #4CAF50',
            'max-width: 800px; margin: 0 auto; padding: 20px'
        ]
        
        # Count matches
        new_matches = sum(1 for indicator in new_template_indicators if indicator in content)
        old_matches = sum(1 for indicator in old_template_indicators if indicator in content)
        
        # Determine template type
        if new_matches >= 3:
            return "new_dark_theme"
        elif old_matches >= 2:
            return "old_basic"
        else:
            return "unknown"
            
    except Exception as e:
        print(f"Error checking {file_path}: {e}")
        return "error"

def analyze_proposals():
    """Analyze all proposals and categorize by template type"""
    
    print("🔍 Analyzing proposal templates...")
    
    # Get all proposal files
    proposal_files = glob.glob(os.path.join(PROPOSALS_DIR, "*.html"))
    
    results = {
        "new_dark_theme": [],
        "old_basic": [],
        "unknown": [],
        "error": []
    }
    
    for file_path in proposal_files:
        filename = os.path.basename(file_path)
        template_type = check_template_type(file_path)
        results[template_type].append({
            "filename": filename,
            "path": file_path,
            "size": os.path.getsize(file_path),
            "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
        })
    
    return results

def filter_proposal_queue(keep_only_new=True):
    """Filter the proposal queue to keep only new template proposals"""
    
    print("📋 Filtering proposal queue...")
    
    # Load current queue
    try:
        with open(QUEUE_FILE, 'r') as f:
            queue = json.load(f)
    except Exception as e:
        print(f"Error loading queue: {e}")
        return
    
    print(f"📊 Current queue has {len(queue)} proposals")
    
    # Analyze proposals to get template types
    results = analyze_proposals()
    new_template_files = {item['filename'] for item in results['new_dark_theme']}
    
    # Filter queue
    filtered_queue = []
    for proposal in queue:
        filename = proposal.get('filename', '')
        if filename in new_template_files:
            proposal['template_type'] = 'new_dark_theme'
            filtered_queue.append(proposal)
        elif not keep_only_new:
            proposal['template_type'] = 'old_basic'
            filtered_queue.append(proposal)
    
    # Backup original queue
    backup_file = f"{QUEUE_FILE}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    with open(backup_file, 'w') as f:
        json.dump(queue, f, indent=2)
    print(f"💾 Backed up original queue to {backup_file}")
    
    # Save filtered queue
    with open(QUEUE_FILE, 'w') as f:
        json.dump(filtered_queue, f, indent=2)
    
    print(f"✅ Filtered queue: {len(filtered_queue)} proposals (was {len(queue)})")
    print(f"🗑️  Removed {len(queue) - len(filtered_queue)} old template proposals from queue")
    
    return filtered_queue

def remove_old_template_files():
    """Remove old template proposal files from both directories"""
    
    print("🗑️  Removing old template files...")
    
    results = analyze_proposals()
    old_files = results['old_basic'] + results['unknown'] + results['error']
    
    removed_count = 0
    
    for file_info in old_files:
        filename = file_info['filename']
        
        # Remove from server directory
        server_path = os.path.join(PROPOSALS_DIR, filename)
        if os.path.exists(server_path):
            os.remove(server_path)
            removed_count += 1
            print(f"   📄 Removed {filename} from server")
        
        # Remove from Netlify directory  
        netlify_path = os.path.join(NETLIFY_PROPOSALS_DIR, filename)
        if os.path.exists(netlify_path):
            os.remove(netlify_path)
            print(f"   📄 Removed {filename} from Netlify")
    
    print(f"🎯 Removed {removed_count} old template files")
    return removed_count

def main():
    """Main function to analyze and filter proposals"""
    
    print("🎨 PROPOSAL TEMPLATE FILTER")
    print("="*50)
    
    # Analyze current proposals
    results = analyze_proposals()
    
    print("\n📊 ANALYSIS RESULTS:")
    print(f"   ✅ New Dark Theme: {len(results['new_dark_theme'])} proposals")
    print(f"   📰 Old Basic: {len(results['old_basic'])} proposals") 
    print(f"   ❓ Unknown: {len(results['unknown'])} proposals")
    print(f"   ❌ Error: {len(results['error'])} proposals")
    
    if results['new_dark_theme']:
        print(f"\n🎨 NEW TEMPLATE PROPOSALS (most recent 5):")
        for proposal in sorted(results['new_dark_theme'], key=lambda x: x['modified'], reverse=True)[:5]:
            print(f"   📄 {proposal['filename']} ({proposal['modified'][:16]})")
    
    if results['old_basic']:
        print(f"\n📰 OLD TEMPLATE PROPOSALS (oldest 5):")
        for proposal in sorted(results['old_basic'], key=lambda x: x['modified'])[:5]:
            print(f"   📄 {proposal['filename']} ({proposal['modified'][:16]})")
    
    # Ask for action
    print(f"\n🎯 RECOMMENDED ACTIONS:")
    print(f"   1. Filter dashboard to show only new template proposals ({len(results['new_dark_theme'])})")
    print(f"   2. Remove old template files entirely ({len(results['old_basic']) + len(results['unknown'])})")
    
    # For automation, let's filter the queue and optionally remove old files
    action = input("\nChoose action (1=filter, 2=remove, 3=both): ").strip()
    
    if action in ['1', '3']:
        filtered_queue = filter_proposal_queue(keep_only_new=True)
        
    if action in ['2', '3']:
        removed_count = remove_old_template_files()
        
    print(f"\n✅ OPERATION COMPLETE!")
    print(f"   📊 Dashboard now shows only new dark theme proposals")
    print(f"   🎨 All proposals use consistent professional design")

if __name__ == "__main__":
    main() 