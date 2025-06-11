#!/usr/bin/env python3
"""
Generate static proposals data for Netlify dashboard
This script reads the proposal queue and generates a static JSON file
that can be committed to git and served by Netlify
"""

import json
import os
from datetime import datetime

# Paths
QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
OUTPUT_FILE = "/root/homelab-docs/projekt-ai-website/data/proposals.json"

def generate_static_data():
    """Generate static proposals data for dashboard"""
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    try:
        # Load proposal queue
        with open(QUEUE_FILE, 'r') as f:
            proposals = json.load(f)
        
        # Sort by timestamp (most recent first)
        if isinstance(proposals, list):
            proposals.sort(key=lambda x: x.get('timestamp', x.get('created_at', '')), reverse=True)
            
            # Limit to last 50 proposals
            proposals = proposals[:50]
        
        # Add metadata
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "total_proposals": len(proposals),
            "proposals": proposals
        }
        
        # Write to output file
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✅ Generated static proposals data: {OUTPUT_FILE}")
        print(f"📊 Total proposals: {len(proposals)}")
        
    except Exception as e:
        print(f"❌ Error generating static data: {e}")
        # Create empty file if error
        with open(OUTPUT_FILE, 'w') as f:
            json.dump({"generated_at": datetime.now().isoformat(), "proposals": []}, f)

if __name__ == "__main__":
    generate_static_data() 