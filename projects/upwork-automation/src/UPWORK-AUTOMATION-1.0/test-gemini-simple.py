#!/usr/bin/env python3
"""
Simple Gemini Test for Upwork Proposals
Tests if Gemini API is working without requiring all dependencies
"""

import os
import sys

# Your Gemini API key
GEMINI_API_KEY = "AIzaSyDd5ZmjEGExtFuiEwhIk15glVGVXjsIjNg"

print("🧪 Testing Gemini API for Upwork Proposals...")
print("=" * 50)

try:
    import google.generativeai as genai
    print("✅ Gemini library is installed")
except ImportError:
    print("❌ Gemini library not installed. Install with:")
    print("   pip3 install google-generativeai --break-system-packages")
    print("\nFor now, let's test with a simple HTTP request...")
    
    # Test with curl command instead
    import subprocess
    
    test_prompt = "Write a one-sentence Upwork proposal opener for a Zapier automation job"
    
    curl_command = f"""curl -s -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}' \
    -H 'Content-Type: application/json' \
    -d '{{"contents":[{{"parts":[{{"text":"{test_prompt}"}}]}}]}}'"""
    
    try:
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("\n✅ Gemini API is working!")
            print("Response preview:", result.stdout[:200], "...")
        else:
            print("❌ API request failed:", result.stderr)
    except Exception as e:
        print("❌ Error testing API:", e)
    
    sys.exit(0)

# If library is installed, test it properly
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

print("\n📝 Testing proposal generation...")

test_job = """
Zapier Expert Needed - Restaurant Automation
We need help connecting our POS system to inventory management.
Budget: $2,000-$5,000
"""

prompt = f"""
You are Timothy Poulton, a 20-year automation specialist.
Write a compelling 100-word Upwork proposal for this job:

{test_job}

Include:
1. Empathy for their pain point
2. Relevant experience metric
3. Clear next step
"""

try:
    response = model.generate_content(prompt)
    print("\n✅ Generated Proposal:")
    print("-" * 50)
    print(response.text)
    print("-" * 50)
    print("\n🎉 Gemini is ready for premium Upwork proposals!")
    
except Exception as e:
    print(f"\n❌ Error generating proposal: {e}")
    print("\nTroubleshooting:")
    print("1. Check if the API key is valid")
    print("2. Ensure you have internet connectivity")
    print("3. Try again in a few seconds")

print("\n💡 To use the full premium system:")
print("1. Install dependencies: pip3 install openai google-generativeai --break-system-packages")
print("2. Add your OpenAI API key to .env file")
print("3. Run: python3 premium_ai_proposal_system_gemini.py") 