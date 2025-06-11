#!/usr/bin/env python3
"""Test script for Premium AI Proposal System with Gemini"""

import asyncio
import json
import sys
import importlib.util
import os

# Dynamically import the hyphenated module
module_path = os.path.join(os.path.dirname(__file__), 'premium-ai-proposal-system-gemini.py')
spec = importlib.util.spec_from_file_location('premium_ai_proposal_system_gemini', module_path)
premium_ai_module = importlib.util.module_from_spec(spec)
sys.modules['premium_ai_proposal_system_gemini'] = premium_ai_module
spec.loader.exec_module(premium_ai_module)

PremiumProposalGenerator = premium_ai_module.PremiumProposalGenerator
ProposalRequest = premium_ai_module.ProposalRequest

async def test_system():
    """Test the premium AI system with a sample job"""
    
    print("🧪 Testing Premium AI Proposal System (Gemini Version)...")
    print("=" * 50)
    
    # Initialize generator
    generator = PremiumProposalGenerator()
    
    # Test job
    test_job = ProposalRequest(
        job_title="Zapier Expert Needed - Automate Our Restaurant Operations",
        job_description="""
        We're a growing restaurant chain (5 locations) drowning in manual processes.
        
        Need help with:
        - Connecting our POS system to inventory management
        - Automating staff scheduling based on sales forecasts
        - Setting up automated customer feedback collection
        - Creating dashboards for each location manager
        
        We use Toast POS, Google Sheets, and Slack. Open to other tools.
        
        Must have experience with restaurant operations. 
        Looking to start ASAP. Budget is flexible for the right person.
        """,
        budget="$2,000 - $5,000",
        required_skills=["Zapier", "API Integration", "Restaurant Systems", "Toast POS"]
    )
    
    # Generate proposal
    print("\n🤖 Generating proposal with GPT-4 + Gemini...")
    result = await generator.generate_premium_proposal(test_job)
    
    # Display results
    print("\n✅ PROPOSAL GENERATED!")
    print("=" * 50)
    print(f"\n📝 Primary Proposal:\n{result['primary_proposal']}")
    print(f"\n📊 Optimization Score: {result['optimization_score']}")
    print(f"\n💡 Personalization Tips:")
    for tip in result['personalization_tips']:
        print(f"   - {tip}")
    
    print("\n🔄 Variations Generated:")
    for var in result['variations']:
        print(f"   - {var['type']}: Score {var['score']}")
    
    print("\n✨ Test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_system()) 