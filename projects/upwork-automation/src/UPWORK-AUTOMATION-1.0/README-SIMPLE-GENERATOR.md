# Simple Upwork Proposal Generator

**Version:** 1.1  
**Date:** June 3, 2025  
**Author:** System Administrator

## Overview

This is a simplified version of the Upwork automation system. It provides a clean web interface for manually generating proposals from Upwork job URLs while also integrating with your existing Chrome extension for job scraping.

## Key Features

1. **Simple Web Interface** - Enter any Upwork job URL and get a proposal instantly
2. **Uses Existing Multi-Model AI** - Leverages the existing multi-model AI system for high-quality proposals
3. **Dark Theme Template** - Uses the same professional dark theme template for consistent branding
4. **Manual Entry Fallback** - Provides a manual entry form when automated scraping is blocked
5. **Chrome Extension Integration** - Displays jobs scraped by your Chrome extension in a list
6. **Job Management** - Accept or reject jobs directly from the interface

## How It Works

The system operates in two modes:

### Manual URL Entry
1. User enters an Upwork job URL in the form
2. System attempts to extract job details (with fallback to manual entry if blocked)
3. Multi-Model AI generates a proposal
4. Proposal is displayed using the dark theme template

### Chrome Extension Integration
1. Chrome extension scrapes jobs and sends them to the webhook
2. Jobs appear in the list on the Simple Generator interface
3. User can select a job to generate a proposal or reject it
4. Generated proposals use the same dark theme template

## Technical Details

- **Port:** 5055
- **Dependencies:** Flask, Requests
- **Multi-Model AI Server:** http://localhost:5001
- **Job Queue File:** proposal-queue.json

## Setup and Running

1. Ensure the multi-model AI server is running
2. Run the simple generator:
   ```
   ./run-simple-generator.sh
   ```
3. Open your browser to http://localhost:5055

## Advantages Over Complex System

1. **Simplified Architecture** - Single web server handles everything
2. **No Automation Required** - Manual control over which jobs get proposals
3. **Upwork Anti-Scraping Workaround** - Manual entry form when automatic extraction fails
4. **Maintains Quality** - Uses the same multi-model AI for proposal generation
5. **Familiar Interface** - Consistent with your existing system's dark theme

## Next Steps and Improvements

- Add authentication to protect the interface
- Implement proposal editing before submission
- Add proposal history and statistics
- Integrate directly with Upwork API (if you have API access)
- Add notification system for new jobs 