#!/usr/bin/env python3
"""
Webhook Capture Utility for Upwork Job Scraper Testing
- Listens on port 5055 (Category E, per PORT-TRACKER.md)
- Captures and logs all POSTed job data from the Chrome extension
- Saves each payload to a timestamped JSON file in this directory
- Adheres to homelab and Cursor standardization rules
"""

from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
import logging

# Configuration
PORT = 5055  # Category E, not in use by production
CAPTURE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(CAPTURE_DIR, 'webhook-capture.log')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

@app.route('/webhook/test-capture', methods=['POST'])
def capture_webhook():
    try:
        data = request.get_json(force=True)
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f'job-capture-{timestamp}.json'
        filepath = os.path.join(CAPTURE_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"✅ Captured job data to {filename}")
        return jsonify({"status": "success", "file": filename}), 200
    except Exception as e:
        logging.error(f"❌ Error capturing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/', methods=['GET'])
def index():
    return f"Webhook capture running. POST job data to http://{request.host}/webhook/test-capture"

if __name__ == '__main__':
    print(f"\n🚀 Webhook capture utility running!")
    print(f"POST job data to: http://0.0.0.0:{PORT}/webhook/test-capture\n")
    app.run(host='0.0.0.0', port=PORT) 