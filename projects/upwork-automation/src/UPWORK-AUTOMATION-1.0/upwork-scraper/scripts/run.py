#!/usr/bin/env python3
"""
Run script for Upwork Scraper & Proposal Generator
"""

import os
import sys
import argparse
import logging

# Add the src directory to the path so we can import our modules
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, os.path.join(project_root, 'src'))

from api import create_app
from config import config

def setup_logging():
    """Configure logging for the application"""
    log_level = getattr(logging, config.LOG_LEVEL)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=config.LOG_FILE if hasattr(config, 'LOG_FILE') else None
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(log_level)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run the Upwork Scraper & Proposal Generator')
    parser.add_argument('--port', type=int, default=getattr(config, 'PORT', 5055),
                        help='Port to run the server on')
    parser.add_argument('--host', type=str, default=getattr(config, 'HOST', '0.0.0.0'),
                        help='Host to run the server on')
    parser.add_argument('--debug', action='store_true', default=getattr(config, 'DEBUG', False),
                        help='Run in debug mode')
    return parser.parse_args()

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import selenium
        import undetected_chromedriver as uc
        import requests
        import sqlalchemy
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Please install all required dependencies with: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if Chrome is installed
    # This is a simple check and might not work on all systems
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    chrome_found = any(os.path.exists(path) for path in chrome_paths)
    if not chrome_found:
        print("Warning: Chrome browser not found in standard locations")
        print("Please ensure Chrome is installed and accessible")

def main():
    """Main entry point for the application"""
    # Parse command line arguments
    args = parse_args()
    
    # Setup logging
    setup_logging()
    
    # Check dependencies
    check_dependencies()
    
    # Log startup information
    logging.info(f"Starting Upwork Scraper & Proposal Generator on {args.host}:{args.port}")
    
    # Create and run the Flask app
    app = create_app()
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )

if __name__ == '__main__':
    main() 