#!/usr/bin/env python3
"""
Test script to verify the full proposal generation flow
"""

import requests
import json
import time
import sys

# Configuration
GENERATOR_URL = "http://localhost:5056"
MULTIMODEL_URL = "http://localhost:5001"

def test_webhook():
    """Test sending a job via webhook"""
    print("1. Testing webhook endpoint...")
    
    job_data = {
        "title": "Full-Stack Developer for E-commerce Platform",
        "client_name": "TechStartup Inc.",
        "budget": "$5,000-$10,000",
        "description": """We're looking for an experienced full-stack developer to help build our e-commerce platform. 
        The project involves:
        - Building a React frontend with modern UI/UX
        - Developing a Node.js/Express backend API
        - Integrating with Stripe for payments
        - Setting up automated inventory management
        - Creating admin dashboard for order management
        
        Must have experience with:
        - React, Node.js, MongoDB
        - Payment gateway integration
        - E-commerce platforms
        - API development
        - Automation tools
        
        This is a 2-3 month project with potential for long-term collaboration.""",
        "url": "https://www.upwork.com/jobs/~test-fullstack-123456",
        "job_id": f"test_fullstack_{int(time.time())}"
    }
    
    response = requests.post(
        f"{GENERATOR_URL}/webhook/rss-jobs",
        json=job_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        print("✅ Job successfully added via webhook")
        print(f"   Response: {response.json()}")
        return job_data["job_id"]
    else:
        print(f"❌ Failed to add job: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_multimodel_direct():
    """Test the multi-model server directly"""
    print("\n2. Testing multi-model server directly...")
    
    job_data = {
        "title": "Python Automation Expert Needed",
        "description": "Need help automating our business processes",
        "budget": "$2,000",
        "client_name": "Business Corp"
    }
    
    try:
        response = requests.post(
            f"{MULTIMODEL_URL}/webhook/job-direct",
            json=job_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Multi-model server responded successfully")
            result = response.json()
            print(f"   Generated proposal score: {result.get('score', 'N/A')}")
            print(f"   Message preview: {result.get('message', '')[:100]}...")
            return True
        else:
            print(f"❌ Multi-model server error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to multi-model server at", MULTIMODEL_URL)
        print("   Make sure upwork-proposal-server-multimodel.py is running")
        return False
    except Exception as e:
        print(f"❌ Error testing multi-model server: {e}")
        return False

def check_dashboard():
    """Check if the dashboard is accessible"""
    print("\n3. Checking dashboard accessibility...")
    
    try:
        response = requests.get(f"{GENERATOR_URL}/")
        if response.status_code == 200:
            print("✅ Dashboard is accessible")
            # Count jobs in the response
            if "job-card" in response.text:
                job_count = response.text.count("job-card")
                print(f"   Found {job_count} jobs displayed")
            return True
        else:
            print(f"❌ Dashboard returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing dashboard: {e}")
        return False

def test_proposal_generation(job_id):
    """Test generating a proposal for a specific job"""
    print(f"\n4. Testing proposal generation for job {job_id}...")
    
    # Simulate form submission
    response = requests.post(
        f"{GENERATOR_URL}/generate-from-queue",
        data={"job_id": job_id},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        print("✅ Proposal generated successfully")
        # Check if it's an HTML response with proposal content
        if "proposal" in response.text.lower() and "html" in response.text.lower():
            print("   Received formatted HTML proposal")
        return True
    else:
        print(f"❌ Failed to generate proposal: {response.status_code}")
        return False

def main():
    print("=== Upwork Proposal Generator Test Suite ===\n")
    
    # Test 1: Add job via webhook
    job_id = test_webhook()
    if not job_id:
        print("\n⚠️  Webhook test failed, but continuing with other tests...")
    
    # Test 2: Test multi-model server
    multimodel_ok = test_multimodel_direct()
    
    # Test 3: Check dashboard
    dashboard_ok = check_dashboard()
    
    # Test 4: Generate proposal if we have a job ID
    if job_id and multimodel_ok:
        time.sleep(1)  # Give the system a moment
        proposal_ok = test_proposal_generation(job_id)
    else:
        print("\n⚠️  Skipping proposal generation test (prerequisites not met)")
        proposal_ok = False
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Webhook:            {'✅ PASS' if job_id else '❌ FAIL'}")
    print(f"Multi-Model Server: {'✅ PASS' if multimodel_ok else '❌ FAIL'}")
    print(f"Dashboard:          {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
    print(f"Proposal Gen:       {'✅ PASS' if proposal_ok else '❌ FAIL'}")
    
    if not multimodel_ok:
        print("\n💡 To start the multi-model server:")
        print("   cd /root/homelab-docs/scripts/upwork-automation")
        print("   python3 upwork-proposal-server-multimodel.py &")

if __name__ == "__main__":
    main() 