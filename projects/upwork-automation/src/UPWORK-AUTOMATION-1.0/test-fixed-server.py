#!/usr/bin/env python3
"""
Test Script for Fixed Upwork Proposal Server
Tests all major fixes: OpenAI API, Client Name Extraction, Enhanced Fallbacks
"""

import requests
import json
import time

def test_server():
    """Test the fixed Upwork proposal server"""
    print("🧪 Testing Fixed Upwork Proposal Server")
    print("=" * 60)
    
    # UPDATED: Use standardized port 5001
    server_url = "http://localhost:5001/webhook/rss-jobs"
    print(f"📡 Sending test jobs to: {server_url}")
    print("")
    
    # Test data with various scenarios
    test_jobs = [
        {
            "title": "Make.com Automation Expert Needed - Connect CRM to Email Marketing",
            "budget": "$2,500",
            "description": """Hi, I'm Sarah from TechStartup Inc. We need help connecting our HubSpot CRM to Mailchimp for automated email campaigns. Currently we manually export leads from HubSpot and import them to Mailchimp every week, which is time-consuming and error-prone. We want to automate this process so new leads automatically get added to appropriate email sequences based on their source and lead score.""",
            "client": {
                "name": "Sarah Johnson",
                "paymentVerified": True,
                "totalSpent": 15000,
                "totalJobsPosted": 12,
                "totalHires": 10,
                "location": {"country": "United States"}
            },
            "proposalsCount": 8,
            "postedTime": "2025-06-01T22:00:00Z"
        },
        {
            "title": "Zapier Workflow for E-commerce Inventory Management",
            "budget": "$1,200",
            "description": """Our team at RetailCorp needs to automate inventory updates between Shopify and our warehouse management system. We're currently updating stock levels manually which leads to overselling. Looking for someone to create Zapier workflows that sync inventory in real-time.""",
            "client": {
                "paymentVerified": True,
                "totalSpent": 8500,
                "totalJobsPosted": 5,
                "totalHires": 4,
                "location": {"country": "Canada"}
            },
            "proposalsCount": 15,
            "postedTime": "2025-06-01T21:30:00Z"
        },
        {
            "title": "WordPress Theme Customization",
            "budget": "$500",
            "description": """Need someone to customize our WordPress theme. Change colors, fonts, and layout. Some CSS knowledge required.""",
            "client": {
                "paymentVerified": False,
                "totalSpent": 200,
                "totalJobsPosted": 2,
                "totalHires": 1,
                "location": {"country": "India"}
            },
            "proposalsCount": 45,
            "postedTime": "2025-06-01T20:00:00Z"
        }
    ]
    
    print()
    
    for i, job in enumerate(test_jobs, 1):
        print(f"🔬 Test {i}: {job['title'][:50]}...")
        
        try:
            # Send job to server
            response = requests.post(
                server_url,
                json=[job],  # Send as list format
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Server Response: {result}")
                
                # Check if proposal was generated
                if result.get('proposals_generated', 0) > 0:
                    print(f"   📝 Proposal generated successfully!")
                else:
                    print(f"   ⏭️ Job skipped (likely low score)")
                    
            else:
                print(f"   ❌ Server Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Connection Error: {e}")
            
        print()
        time.sleep(2)  # Brief pause between tests
    
    # Test edge cases
    print("🔬 Testing Edge Cases:")
    print("-" * 30)
    
    # Test with missing client data
    edge_case_job = {
        "title": "n8n Integration Project",
        "budget": "$1,500",
        "description": "Hello, we need help with our workflows.",
        "client": {},  # Empty client data to test name extraction
        "proposalsCount": 5
    }
    
    print("🔬 Edge Case: Missing client data...")
    try:
        response = requests.post(
            server_url,
            json=[edge_case_job],
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Handled gracefully: {result}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print()
    print("🎯 Test Summary:")
    print("   Check the proposals directory: /srv/apps/client-proposals/public/")
    print("   Check the queue file: scripts/upwork-automation/proposal-queue.json")
    print("   Look for client names other than 'Your Company'")
    print("   Verify AI-generated content quality")
    print()
    print("✅ Testing complete!")

if __name__ == "__main__":
    test_server() 