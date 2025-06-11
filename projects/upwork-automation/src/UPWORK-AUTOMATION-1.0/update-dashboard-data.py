#!/usr/bin/env python3
import json
from datetime import datetime

# Load current proposals
with open('/root/homelab-docs/scripts/upwork-automation/proposal-queue.json', 'r') as f:
    proposals = json.load(f)

# Create dashboard data format
dashboard_data = {
    'proposals': proposals,
    'generated_at': datetime.now().isoformat(),
    'total_count': len(proposals)
}

# Update website data file
with open('/root/homelab-docs/projekt-ai-website/data/proposals.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print(f'✅ Updated dashboard data: {len(proposals)} proposals')
print(f'📅 Generated at: {dashboard_data["generated_at"]}') 