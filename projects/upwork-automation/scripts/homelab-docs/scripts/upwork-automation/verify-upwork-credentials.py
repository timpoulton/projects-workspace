#!/usr/bin/env python3
"""
Verify Upwork credentials are correctly loaded
"""
import sys
import os
sys.path.append('/root/homelab-docs/scripts/upwork-automation/upwork-scraper/src')

from config import config

print("Checking Upwork credentials configuration...")
print("-" * 50)

# Check if credentials file exists
cred_file = "/root/homelab-docs/scripts/upwork-automation/upwork-credentials.env"
if os.path.exists(cred_file):
    print(f"✅ Credentials file exists: {cred_file}")
else:
    print(f"❌ Credentials file NOT found: {cred_file}")

# Check loaded credentials (masked for security)
print("\nLoaded credentials:")
print(f"UPWORK_USER_NAME: {config.UPWORK_USER_NAME}")
print(f"UPWORK_USERNAME: {config.UPWORK_USERNAME[:3]}...{config.UPWORK_USERNAME[-10:] if len(config.UPWORK_USERNAME) > 13 else '***'}")
print(f"UPWORK_PASSWORD: {'*' * len(config.UPWORK_PASSWORD) if config.UPWORK_PASSWORD != 'password' else 'NOT SET'}")

# Check if defaults are still in place
if config.UPWORK_USERNAME == "username@example.com":
    print("\n⚠️  WARNING: Using default username. Please update your credentials!")
if config.UPWORK_PASSWORD == "password":
    print("\n⚠️  WARNING: Using default password. Please update your credentials!")
if config.UPWORK_USER_NAME == "User":
    print("\n⚠️  WARNING: Using default user name. Please update with your Upwork first name!")

print("\n" + "-" * 50)
print("Make sure your credentials match your Upwork login exactly.") 