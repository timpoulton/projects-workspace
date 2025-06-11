#!/usr/bin/env python3
"""
Test Upwork login credentials
"""
import sys
import os
sys.path.append('/root/homelab-docs/scripts/upwork-automation/upwork-scraper/src')

from scraper.upwork_scraper import UpworkScraper

# Create scraper instance
scraper = UpworkScraper()

print("Testing Upwork login...")
print("This will open a Chrome browser window.")
print("Watch the browser to see what happens during login.")
print("-" * 50)

# Try to login
success = scraper.login()

if success:
    print("✅ Login successful!")
    print("The scraper was able to log into Upwork.")
else:
    print("❌ Login failed!")
    print("Check the browser window for any errors.")
    print("Common issues:")
    print("- CAPTCHA verification required")
    print("- 2FA enabled on your account")
    print("- Incorrect credentials")
    print("- Upwork has changed their login page")

# Keep browser open for inspection
input("\nPress Enter to close the browser...")
scraper.close() 