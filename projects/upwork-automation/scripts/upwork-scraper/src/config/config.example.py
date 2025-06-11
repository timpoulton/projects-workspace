"""
Configuration file for Upwork Scraper & Proposal Generator.
Copy this file to config.py and update with your settings.
"""

# Web application settings
PORT = 5055
HOST = "0.0.0.0"
DEBUG = True
SECRET_KEY = "change-this-to-a-random-string"

# Database settings
DATABASE_PATH = "upwork_scraper.db"

# Upwork credentials
UPWORK_USER_NAME = "Your Name"  # First name shown on Upwork profile
UPWORK_USERNAME = "your.email@example.com"
UPWORK_PASSWORD = "your-password"

# Chrome driver settings
CHROME_VERSIONS = [
    90,
    91,
    92,
    123,
]
MAX_ATTEMPTS = 3
HEADLESS = True  # Set to False to see the browser window during scraping

# Multi-Model AI server
MULTIMODEL_SERVER = "http://localhost:5001"
MULTIMODEL_TIMEOUT = 60  # seconds

# Scraping settings
SCRAPE_DELAY = 2  # seconds between page interactions
MAX_JOBS = 20  # maximum number of jobs to scrape per search
SCROLL_PAUSE_TIME = 1.5  # seconds to pause between scrolls

# Proposal settings
TEMPLATE_PATH = "../templates/dark-proposal-template.html"
FALLBACK_TEMPLATE_PATH = "../templates/simple-proposal-template.html"

# User preferences
DEFAULT_SKILLS = [
    "Python",
    "Automation",
    "Web Scraping",
    "API Integration",
]

# Search settings
DEFAULT_SEARCH_TERMS = "Python automation"
MINIMUM_BUDGET = 100  # Minimum budget to consider

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "upwork_scraper.log" 