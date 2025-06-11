#!/usr/bin/env python3
"""
Clear All Proposals Script
Removes all existing proposals since they use the old template
New proposals will use the new dark theme template
"""

import json
import os
import glob

QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
SERVER_PROPOSALS_DIR = "/var/www/projekt-ai.net/proposals/"
NETLIFY_PROPOSALS_DIR = "/root/homelab-docs/projekt-ai-website/proposals/"

def clear_all_proposals():
    """Clear all existing proposals from dashboard and directories"""
    
    print("🧹 CLEARING ALL OLD TEMPLATE PROPOSALS")
    print("📋 This will remove all current jobs from the dashboard")
    print("✨ New jobs will use the new dark theme template")
    print()
    
    # 1. Clear the proposal queue (dashboard data)
    print("1️⃣ Clearing proposal queue...")
    try:
        with open(QUEUE_FILE, 'w') as f:
            json.dump([], f, indent=2)
        print("   ✅ Proposal queue cleared (dashboard will show 0 jobs)")
    except Exception as e:
        print(f"   ❌ Error clearing queue: {e}")
    
    # 2. Archive existing server proposals
    print("\n2️⃣ Archiving server proposals...")
    server_files = glob.glob(os.path.join(SERVER_PROPOSALS_DIR, "*.html"))
    if server_files:
        archive_dir = f"{SERVER_PROPOSALS_DIR}archived-old-template/"
        os.makedirs(archive_dir, exist_ok=True)
        
        moved_count = 0
        for file_path in server_files:
            filename = os.path.basename(file_path)
            archive_path = os.path.join(archive_dir, filename)
            try:
                os.rename(file_path, archive_path)
                moved_count += 1
            except Exception as e:
                print(f"   ⚠️ Error moving {filename}: {e}")
        
        print(f"   ✅ Archived {moved_count} server proposals to {archive_dir}")
    else:
        print("   ✅ No server proposals to archive")
    
    # 3. Archive Netlify proposals
    print("\n3️⃣ Archiving Netlify proposals...")
    netlify_files = glob.glob(os.path.join(NETLIFY_PROPOSALS_DIR, "*.html"))
    if netlify_files:
        archive_dir = f"{NETLIFY_PROPOSALS_DIR}archived-old-template/"
        os.makedirs(archive_dir, exist_ok=True)
        
        moved_count = 0
        for file_path in netlify_files:
            filename = os.path.basename(file_path)
            archive_path = os.path.join(archive_dir, filename)
            try:
                os.rename(file_path, archive_path)
                moved_count += 1
            except Exception as e:
                print(f"   ⚠️ Error moving {filename}: {e}")
        
        print(f"   ✅ Archived {moved_count} Netlify proposals to {archive_dir}")
    else:
        print("   ✅ No Netlify proposals to archive")
    
    # 4. Update web queue for dashboard
    print("\n4️⃣ Updating web dashboard data...")
    web_queue = "/srv/apps/client-proposals/public/proposal-queue.json"
    try:
        os.makedirs(os.path.dirname(web_queue), exist_ok=True)
        with open(web_queue, 'w') as f:
            json.dump([], f, indent=2)
        print("   ✅ Web dashboard data cleared")
    except Exception as e:
        print(f"   ⚠️ Error updating web queue: {e}")
    
    print("\n🎯 CLEANUP COMPLETE!")
    print("   📊 Dashboard now shows 0 jobs")
    print("   📁 Old proposals archived (not deleted)")
    print("   ✨ Ready for new dark theme proposals")
    print("   🚀 Next proposals will use the new template")

if __name__ == "__main__":
    clear_all_proposals() 