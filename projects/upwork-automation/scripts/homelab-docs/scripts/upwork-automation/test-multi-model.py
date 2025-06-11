#!/usr/bin/env python3
"""
Test Multi-Model AI Server
Send a sample job to verify advanced scoring and AI generation
"""

import json
import requests

# Test job data
test_job = {
    "title": "Automate Restaurant POS Integration with Make.com and Zapier",
    "description": """
    We need to automate our restaurant operations by integrating our POS system with our booking platform, 
    inventory management, and customer communications. Currently doing everything manually which is 
    time-consuming and error-prone. 
    
    Looking for someone experienced with Make.com, Zapier, or similar automation platforms to:
    - Connect our Square POS to our booking system
    - Automate inventory alerts when items run low  
    - Set up automated customer follow-up emails
    - Create reporting dashboards
    
    Budget: $2000-3000
    Timeline: 2-3 weeks
    """,
    "budget": "$2000-3000",
    "client": "Restaurant Owner",
    "guid": "test-job-12345",
    "link": "https://upwork.com/test-job"
}

def test_multi_model_server():
    """Test the multi-model server with sample job"""
    
    url = "http://192.168.1.107:5001/webhook/rss-jobs"
    
    print("🧪 TESTING MULTI-MODEL AI SERVER")
    print(f"📡 Sending test job to: {url}")
    print(f"📋 Job Title: {test_job['title']}")
    print(f"💰 Budget: {test_job['budget']}")
    print()
    
    try:
        # Send test job
        response = requests.post(url, json=[test_job], timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"📈 Total Jobs: {result.get('total_jobs', 0)}")
            print(f"✔️ Processed: {result.get('processed', 0)}")
            print(f"❌ Rejected: {result.get('rejected', 0)}")
            print(f"🤖 AI Models Available:")
            ai_models = result.get('ai_models_used', {})
            for model, available in ai_models.items():
                status = "✅" if available else "❌"
                print(f"   • {model.upper()}: {status}")
            
            # Check if proposal was created
            if result.get('processed', 0) > 0:
                print(f"\n🎯 MULTI-MODEL AI PROPOSAL GENERATED!")
                print(f"🔍 Check the latest proposals to see multi-model output")
            else:
                print(f"\n⚠️ Job was rejected by scoring system")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def check_latest_proposals():
    """Check the latest proposals from both servers"""
    
    print(f"\n📋 CHECKING LATEST PROPOSALS:")
    
    try:
        # Check multi-model server
        response = requests.get("http://192.168.1.107:5001/api/proposals")
        if response.status_code == 200:
            proposals = response.json()
            latest = proposals[0] if proposals else None
            
            if latest:
                print(f"\n🤖 LATEST MULTI-MODEL PROPOSAL:")
                print(f"   Title: {latest.get('job_title', 'N/A')[:50]}...")
                print(f"   Score: {latest.get('score', 'N/A')}")
                print(f"   AI Model: {latest.get('ai_model_used', 'N/A')}")
                print(f"   Server: {latest.get('server_version', 'N/A')}")
                print(f"   Created: {latest.get('created_at', 'N/A')}")
                
                # Show analysis details if available
                analysis = latest.get('analysis', {})
                if analysis:
                    print(f"   Analysis Type: {analysis.get('analysis_type', 'N/A')}")
                    print(f"   Automation Terms: {analysis.get('automation_terms_found', 'N/A')}")
                    print(f"   Tools: {', '.join(analysis.get('tools', []))}")
    
    except Exception as e:
        print(f"❌ Error checking proposals: {e}")

if __name__ == "__main__":
    test_multi_model_server()
    check_latest_proposals() 