#!/usr/bin/env python3
"""
Test script to send a sample job to the webhook endpoint
"""

import requests
import json
import time

# Webhook URL
WEBHOOK_URL = "http://localhost:5056/webhook/rss-jobs"

# Sample job data (similar to what Chrome extension would send)
sample_job = {
    "title": "Python Developer Needed for Automation Project",
    "client_name": "Test Client",
    "budget": "$500-$1000",
    "description": "We need an experienced Python developer to help build an automation system for our business processes. The ideal candidate should have experience with web scraping, API integration, and workflow automation.",
    "url": "https://www.upwork.com/jobs/~test123456",
    "job_id": f"test_job_{int(time.time())}"
}

print(f"Sending test job to webhook: {WEBHOOK_URL}")
print(f"Job title: {sample_job['title']}")

try:
    response = requests.post(WEBHOOK_URL, json=sample_job)
    print(f"\nResponse status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ Job successfully sent to webhook!")
        print("Check the dashboard to see the job")
    else:
        print("\n❌ Failed to send job to webhook")
        
except Exception as e:
    print(f"\n❌ Error sending job: {e}") 