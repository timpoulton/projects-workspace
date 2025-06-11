"""
Routes for the Upwork Scraper & Proposal Generator
"""

import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app

from scraper.upwork_scraper import UpworkScraper
from utils.db import get_db, save_job, save_proposal, get_jobs, get_job_by_id, update_job_status
from utils.helpers import generate_proposal

# Create blueprint
main_bp = Blueprint('main', __name__)

# Set up logger
logger = logging.getLogger(__name__)

@main_bp.route('/')
def index():
    """Main page with search form and job list"""
    # Get jobs from database
    jobs = get_jobs(status='pending')
    return render_template('index.html', jobs=jobs)

@main_bp.route('/search', methods=['POST'])
def search():
    """Handle job search"""
    search_query = request.form.get('search_query', '')
    
    if not search_query:
        flash('Please enter a search query', 'error')
        return redirect(url_for('main.index'))
    
    try:
        # Initialize scraper
        scraper = UpworkScraper()
        
        # Login to Upwork
        if not scraper.login():
            flash('Failed to login to Upwork. Please check your credentials.', 'error')
            return redirect(url_for('main.index'))
        
        # Search for jobs
        jobs = scraper.search_jobs(search_query)
        
        # Save jobs to database
        for job in jobs:
            save_job(job)
        
        flash(f'Found {len(jobs)} jobs matching your query', 'success')
        return redirect(url_for('main.index'))
    
    except Exception as e:
        logger.error(f"Error during job search: {e}")
        flash(f'Error during job search: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@main_bp.route('/job/<job_id>')
def view_job(job_id):
    """View job details"""
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('job_details.html', job=job)

@main_bp.route('/generate/<job_id>', methods=['POST'])
def generate(job_id):
    """Generate proposal for a job"""
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('main.index'))
    
    try:
        # Generate proposal using multi-model AI
        proposal_data = generate_proposal(job)
        
        # Save proposal to database
        save_proposal(job_id, proposal_data)
        
        # Update job status to processed
        update_job_status(job_id, 'processed')
        
        # Redirect to proposal view
        return redirect(url_for('main.view_proposal', job_id=job_id))
    
    except Exception as e:
        logger.error(f"Error generating proposal: {e}")
        flash(f'Error generating proposal: {str(e)}', 'error')
        return redirect(url_for('main.view_job', job_id=job_id))

@main_bp.route('/proposal/<job_id>')
def view_proposal(job_id):
    """View generated proposal"""
    job = get_job_by_id(job_id)
    if not job:
        flash('Job not found', 'error')
        return redirect(url_for('main.index'))
    
    if job.get('status') != 'processed':
        flash('No proposal has been generated for this job yet', 'error')
        return redirect(url_for('main.view_job', job_id=job_id))
    
    return render_template('proposal.html', job=job, proposal=job.get('proposal'))

@main_bp.route('/reject/<job_id>', methods=['POST'])
def reject_job(job_id):
    """Reject a job"""
    update_job_status(job_id, 'rejected')
    flash('Job rejected', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/api/jobs')
def api_jobs():
    """API endpoint to get jobs"""
    status = request.args.get('status', 'pending')
    jobs = get_jobs(status=status)
    return jsonify(jobs)

@main_bp.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint to generate proposal"""
    data = request.json
    job_id = data.get('job_id')
    
    if not job_id:
        return jsonify({'error': 'No job ID provided'}), 400
    
    job = get_job_by_id(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    try:
        # Generate proposal
        proposal_data = generate_proposal(job)
        
        # Save proposal
        save_proposal(job_id, proposal_data)
        
        # Update job status
        update_job_status(job_id, 'processed')
        
        return jsonify(proposal_data)
    
    except Exception as e:
        logger.error(f"API error generating proposal: {e}")
        return jsonify({'error': str(e)}), 500 