#!/usr/bin/env python3
"""
Simple API Server for Upwork Dashboard
- Serves proposal data with proper headers
- Prevents caching issues
- Handles CORS correctly
"""

from flask import Flask, jsonify, request, make_response
import json
import os
from datetime import datetime
import logging

# Configuration
PORT = 5052  # Use a different port to avoid conflicts
QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
LOG_FILE = "/root/homelab-docs/scripts/upwork-automation/api-server.log"

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Flask app
app = Flask(__name__)

def load_proposals():
    """Load proposals from the queue file"""
    try:
        with open(QUEUE_FILE, 'r') as f:
            proposals = json.load(f)
        
        # Ensure it's a list
        if not isinstance(proposals, list):
            logging.warning(f"Proposals data is not a list: {type(proposals)}")
            return []
            
        return proposals
    except Exception as e:
        logging.error(f"Error loading proposals: {str(e)}")
        return []

@app.route('/api/proposals', methods=['GET'])
def get_proposals():
    """API endpoint to get proposals with proper headers"""
    
    # Load the data
    proposals = load_proposals()
    logging.info(f"Loaded {len(proposals)} proposals")
    
    # Create response data with timestamp and version
    response_data = {
        "proposals": proposals,
        "generated_at": datetime.now().isoformat(),
        "total_count": len(proposals),
        "version": datetime.now().strftime("%Y%m%d%H%M%S")
    }
    
    # Create response with headers
    resp = make_response(jsonify(response_data))
    
    # Set CORS headers
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    # Set cache control headers
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    
    # Log the request
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    logging.info(f"Served {len(proposals)} proposals to {client_ip} - {user_agent}")
    
    return resp

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "proposal-api"
    })

if __name__ == '__main__':
    # Log startup
    logging.info(f"Starting API server on port {PORT}")
    print(f"🚀 Starting API server on port {PORT}")
    print(f"📋 Using queue file: {QUEUE_FILE}")
    print(f"📝 Logging to: {LOG_FILE}")
    print(f"🔗 API endpoints:")
    print(f"   • http://localhost:{PORT}/api/proposals")
    print(f"   • http://localhost:{PORT}/api/health")
    
    # Run the app
    app.run(host='0.0.0.0', port=PORT) 