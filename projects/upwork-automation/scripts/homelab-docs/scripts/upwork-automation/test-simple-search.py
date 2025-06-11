#!/usr/bin/env python3
"""
Simple test to check Upwork search functionality
"""
import requests
import json

print("Testing Upwork search API...")
print("-" * 50)

# Test the search API
url = "http://localhost:5056/api/search"
data = {
    "query": "Python developer",
    "filters": {}
}

print(f"Sending search request to: {url}")
print(f"Query: {data['query']}")

try:
    response = requests.post(url, json=data, timeout=60)
    print(f"\nResponse status: {response.status_code}")
    
    result = response.json()
    print(f"Success: {result.get('success', False)}")
    
    if result.get('success'):
        jobs = result.get('jobs', [])
        print(f"Number of jobs found: {len(jobs)}")
        
        if jobs:
            print("\nFirst job:")
            job = jobs[0]
            print(f"  Title: {job.get('job_title', 'N/A')}")
            print(f"  Client: {job.get('client_name', 'N/A')}")
            print(f"  Budget: {job.get('budget', 'N/A')}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
        
except Exception as e:
    print(f"Error making request: {e}")

print("\n" + "-" * 50)
print("Check the server logs for more details:") 