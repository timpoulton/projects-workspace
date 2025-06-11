#!/usr/bin/env python3
"""
Test the new filtering system to ensure it properly rejects VA/developer jobs
and accepts AI automation jobs
"""

import requests
import json
import time

SERVER_URL = "http://localhost:5001/webhook/rss-jobs"

# Test job data - should be REJECTED
rejected_jobs = [
    {
        "title": "Virtual Assistant Needed for Administrative Tasks",
        "description": "Looking for a virtual assistant to help with data entry, email management, and scheduling appointments. No automation needed.",
        "budget": "$500",
        "guid": "test-va-1",
        "link": "https://example.com/job1"
    },
    {
        "title": "Full Stack Developer for E-commerce Website", 
        "description": "Need a full stack developer to build a React frontend and Node.js backend for our e-commerce site. Experience with MongoDB required.",
        "budget": "$2000",
        "guid": "test-dev-1",
        "link": "https://example.com/job2"
    },
    {
        "title": "Data Entry Specialist for Manual Work",
        "description": "Looking for someone to manually enter data from PDFs into Excel spreadsheets. Copy paste work, no automation required.",
        "budget": "$300",
        "guid": "test-data-1", 
        "link": "https://example.com/job3"
    }
]

# Test job data - should be ACCEPTED
accepted_jobs = [
    {
        "title": "Make.com Automation Expert for Workflow Integration",
        "description": "Need an automation specialist to build complex workflows using Make.com. Must integrate multiple systems including CRM, email marketing, and webhooks for our business automation needs.",
        "budget": "$1500", 
        "guid": "test-auto-1",
        "link": "https://example.com/job4"
    },
    {
        "title": "AI Agent Development for Customer Support Chatbot",
        "description": "Looking for an AI automation expert to develop an intelligent chatbot using n8n and OpenAI API. Need to automate customer support workflows and integrate with our existing systems.",
        "budget": "$2500",
        "guid": "test-ai-1", 
        "link": "https://example.com/job5"
    },
    {
        "title": "Webflow Automation with Meta Graph API Integration",
        "description": "Seeking automation specialist to build Webflow CMS automation that connects to Facebook and Instagram APIs. Need to automate social media content publishing workflow.",
        "budget": "$1800",
        "guid": "test-webflow-1",
        "link": "https://example.com/job6" 
    }
]

def test_jobs(jobs, expected_result):
    """Test a batch of jobs and check if they're handled as expected"""
    
    print(f"\n🧪 Testing {len(jobs)} jobs - Expected: {expected_result}")
    
    try:
        response = requests.post(SERVER_URL, json=jobs, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            total_jobs = result.get('total_jobs', 0)
            processed = result.get('processed', 0) 
            rejected = result.get('rejected', 0)
            
            print(f"📊 Results: {total_jobs} total, {processed} processed, {rejected} rejected")
            
            if expected_result == "REJECTED":
                if rejected == len(jobs) and processed == 0:
                    print("✅ PASS: All jobs correctly rejected")
                    return True
                else:
                    print("❌ FAIL: Expected all jobs to be rejected")
                    return False
            elif expected_result == "ACCEPTED":
                if processed == len(jobs) and rejected == 0:
                    print("✅ PASS: All jobs correctly accepted")
                    return True
                else:
                    print("❌ FAIL: Expected all jobs to be accepted")
                    return False
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run all filtering tests"""
    
    print("🚀 TESTING NEW FILTERING SYSTEM")
    print("=" * 50)
    
    # Test rejected jobs
    rejected_pass = test_jobs(rejected_jobs, "REJECTED")
    
    # Small delay between tests
    time.sleep(2)
    
    # Test accepted jobs  
    accepted_pass = test_jobs(accepted_jobs, "ACCEPTED")
    
    print("\n" + "=" * 50)
    print("📋 FINAL RESULTS:")
    print(f"❌ Rejection Tests: {'PASS' if rejected_pass else 'FAIL'}")
    print(f"✅ Acceptance Tests: {'PASS' if accepted_pass else 'FAIL'}")
    
    if rejected_pass and accepted_pass:
        print("\n🎉 ALL TESTS PASSED! Filtering system is working correctly.")
        print("✅ VA jobs are being blocked")
        print("✅ Developer jobs are being blocked") 
        print("✅ Automation jobs are being accepted")
    else:
        print("\n⚠️  SOME TESTS FAILED! Check the filtering configuration.")
    
    return rejected_pass and accepted_pass

if __name__ == "__main__":
    main() 