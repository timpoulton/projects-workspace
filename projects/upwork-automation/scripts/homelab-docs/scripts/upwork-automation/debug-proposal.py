#!/usr/bin/env python3
import requests
import json

# Test job that should pass scoring
job_data = {
    'job_title': 'Automate Restaurant Inventory with Make.com',
    'description': 'Need automation expert to integrate our POS with inventory system using Make.com workflows',
    'budget': '$3000',
    'client_name': 'Restaurant Group',
    'job_id': 'test_debug_123'
}

print("Testing proposal generation...")
print(f"Job: {job_data['job_title']}")

# Send to multi-model AI
response = requests.post('http://localhost:5001/webhook/job-direct', json=job_data)
result = response.json()

print('\nMulti-model AI response:')
print(f'Score: {result.get("score")}')
print(f'Message field exists: {"message" in result}')
print(f'Message length: {len(result.get("message", ""))} chars')
print(f'\nMessage content:')
print('-' * 50)
print(result.get("message", "NO MESSAGE FOUND"))
print('-' * 50)

# Now test the simple generator
print("\n\nTesting simple generator formatting...")
# Simulate what happens in generate_from_queue
proposal_data = result.copy()
proposal_data['job_title'] = job_data['job_title']
proposal_data['client_name'] = job_data['client_name']
proposal_data['budget'] = job_data['budget']

print(f"\nProposal data keys: {list(proposal_data.keys())}")
print(f"Message in proposal_data: {'message' in proposal_data}") 