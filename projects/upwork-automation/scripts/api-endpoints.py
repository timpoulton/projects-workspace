#!/usr/bin/env python3
"""
API Endpoints for Upwork Dashboard
Handles approve, reject, and edit actions for proposals
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs
import requests

PORT = 8090  # API endpoint port

class DashboardAPIHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests from dashboard"""
        path = urlparse(self.path).path
        
        if path == '/api/proposals/approve':
            self.handle_approve()
        elif path == '/api/proposals/reject':
            self.handle_reject()
        elif path == '/api/proposals/edit':
            self.handle_edit()
        else:
            self.send_error(404, "Endpoint not found")
    
    def handle_approve(self):
        """Handle proposal approval"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            proposal_id = data.get('id')
            message = data.get('message', '')
            
            # Log the approval
            print(f"✅ Approved proposal: {proposal_id}")
            print(f"📧 Message to send: {message[:100]}...")
            
            # In production, this would:
            # 1. Send the proposal message to Upwork
            # 2. Update the proposal status in database
            # 3. Log the action
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': True, 'id': proposal_id, 'status': 'approved'}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_reject(self):
        """Handle proposal rejection"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            proposal_id = data.get('id')
            
            # Log the rejection
            print(f"❌ Rejected proposal: {proposal_id}")
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': True, 'id': proposal_id, 'status': 'rejected'}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_edit(self):
        """Handle proposal edit/regeneration"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            proposal_id = data.get('id')
            feedback = data.get('feedback', '')
            original_job = data.get('originalJob', {})
            
            print(f"✏️ Edit request for proposal: {proposal_id}")
            print(f"📝 Feedback: {feedback}")
            
            # Send the edit request to the Upwork automation server
            # This will regenerate the proposal with the given feedback
            edit_payload = {
                'job_id': proposal_id,
                'title': original_job.get('title', ''),
                'description': original_job.get('description', ''),
                'budget': original_job.get('budget', ''),
                'client': {'name': original_job.get('client', '')},
                'edit_feedback': feedback
            }
            
            # Send to the Upwork automation server
            try:
                response = requests.post(
                    'http://localhost:5001/webhook/rss-jobs',
                    json=[edit_payload],
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_data = {'success': True, 'id': proposal_id, 'status': 'regenerated'}
                    self.wfile.write(json.dumps(response_data).encode())
                else:
                    self.send_error(500, "Failed to regenerate proposal")
                    
            except Exception as e:
                print(f"Error calling automation server: {e}")
                self.send_error(500, "Failed to connect to automation server")
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def end_headers(self):
        """Add CORS headers to all responses"""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run_api_server():
    """Start the API server"""
    print(f"🚀 Dashboard API Server running on port {PORT}")
    print(f"📡 Endpoints:")
    print(f"   POST /api/proposals/approve")
    print(f"   POST /api/proposals/reject")
    print(f"   POST /api/proposals/edit")
    
    with socketserver.TCPServer(("", PORT), DashboardAPIHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    run_api_server() 