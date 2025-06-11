#!/usr/bin/env python3
"""
Simple API Server for Upwork Dashboard
- Serves proposal data with proper headers
- Prevents caching issues
- Handles CORS correctly for cross-domain access
- Supports the multi-model AI proposal system
"""

from flask import Flask, jsonify, request, make_response
import json
import os
from datetime import datetime
import logging
import sys

# Configuration
PORT = 5050  # Use a different port to avoid conflicts
QUEUE_FILE = "/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
LOG_FILE = "/root/homelab-docs/scripts/upwork-automation/api-server.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

# Initialize Flask app
app = Flask(__name__)

def load_proposals():
    """Load proposals from the queue file"""
    try:
        if not os.path.exists(QUEUE_FILE):
            logging.warning(f"Queue file not found: {QUEUE_FILE}")
            return []
            
        with open(QUEUE_FILE, 'r') as f:
            proposals = json.load(f)
        
        # Ensure it's a list
        if not isinstance(proposals, list):
            logging.warning(f"Proposals data is not a list: {type(proposals)}")
            return []
            
        # Sort by timestamp (most recent first)
        proposals.sort(key=lambda x: x.get('timestamp', x.get('created_at', '')), reverse=True)
        return proposals
    except Exception as e:
        logging.error(f"Error loading proposals: {str(e)}")
        return []

def add_cors_headers(response):
    """Add CORS headers to allow access from any domain"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Origin, Authorization'
    return response

@app.route('/api/proposals', methods=['GET', 'OPTIONS'])
def get_proposals():
    """API endpoint to get proposals with proper headers"""
    
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        resp = make_response()
        return add_cors_headers(resp)
    
    # Load the data
    proposals = load_proposals()
    logging.info(f"Loaded {len(proposals)} proposals")
    
    # Create response data with timestamp and version
    response_data = {
        "proposals": proposals,
        "generated_at": datetime.now().isoformat(),
        "total_count": len(proposals),
        "version": datetime.now().strftime("%Y%m%d%H%M%S"),
        "source": "api.projekt-ai.net"
    }
    
    # Create response with headers
    resp = make_response(jsonify(response_data))
    
    # Add CORS headers
    resp = add_cors_headers(resp)
    
    # Set cache control headers
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    
    # Log the request
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    logging.info(f"Served {len(proposals)} proposals to {client_ip} - {user_agent}")
    
    return resp

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    """Health check endpoint"""
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        resp = make_response()
        return add_cors_headers(resp)
        
    # Check if queue file exists
    queue_exists = os.path.exists(QUEUE_FILE)
    
    resp = make_response(jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "upwork-proposal-api",
        "queue_file_exists": queue_exists,
        "environment": "production"
    }))
    
    # Add CORS headers
    resp = add_cors_headers(resp)
    
    return resp

@app.route('/api/status', methods=['GET', 'OPTIONS'])
def status_check():
    """Simple status endpoint for connectivity testing"""
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        resp = make_response()
        return add_cors_headers(resp)
        
    resp = make_response(jsonify({
        "status": "online",
        "service": "upwork-proposal-api",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }))
    
    # Add CORS headers
    resp = add_cors_headers(resp)
    
    return resp

@app.errorhandler(Exception)
def handle_error(e):
    """Global error handler"""
    logging.error(f"Uncaught exception: {str(e)}")
    resp = make_response(jsonify({
        "status": "error",
        "message": str(e),
        "timestamp": datetime.now().isoformat()
    }), 500)
    return add_cors_headers(resp)

if __name__ == '__main__':
    # Log startup
    logging.info(f"Starting API server on port {PORT}")
    print(f"🚀 Starting API server on port {PORT}")
    print(f"📋 Using queue file: {QUEUE_FILE}")
    print(f"📝 Logging to: {LOG_FILE}")
    print(f"🔗 API endpoints:")
    print(f"   • http://localhost:{PORT}/api/proposals")
    print(f"   • http://localhost:{PORT}/api/health")
    print(f"   • http://localhost:{PORT}/api/status")
    print(f"🌐 CORS: Allowing requests from all origins (*)")
    
    # Run the app
    app.run(host='0.0.0.0', port=PORT, threaded=True) 