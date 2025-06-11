const express = require('express');
const router = express.Router();
const { Event, Guest } = require('../models');
const axios = require('axios');

// Get configuration from environment variables
const WEBFLOW_WEBHOOK_SECRET = process.env.WEBFLOW_WEBHOOK_SECRET || '9beb0bcdcc51ef40cffc539947b47055898885e96931d0bb0a5009ab4696e6a6';
// Add the new Webflow-generated secret
const WEBFLOW_NEW_SECRET = '7ba02129304569b5b6edbc622b1600371e9cb9e46bd5f760f701450d4aa09899';
// Add the latest webhook secret
const WEBFLOW_LATEST_SECRET = '0d8407d1b4b666174c5ed34d15be9376c7b62773b1cb3655511edeeb41c30b63';
// Add the newest Webflow-generated secret (2025-05-25)
const WEBFLOW_CURRENT_SECRET = '5dd664b9f7f4413663d7e133b33b29475c953c8b5948e8b0e6877275f089d6de';
const MAILCHIMP_API_KEY = process.env.MAILCHIMP_API_KEY || '2692c472af4f17326f5c1384a61b4c5b-us12';
const MAILCHIMP_SERVER = process.env.MAILCHIMP_SERVER || 'us12';
const MAILCHIMP_LIST_ID = process.env.MAILCHIMP_LIST_ID || '53f56e2c77';

console.log('-------------------------');
console.log('Webhook module loaded with secrets:');
console.log(`- Original secret: ${WEBFLOW_WEBHOOK_SECRET.substring(0, 10)}...`);
console.log(`- New secret: ${WEBFLOW_NEW_SECRET.substring(0, 10)}...`);
console.log(`- Latest secret: ${WEBFLOW_LATEST_SECRET.substring(0, 10)}...`);
console.log(`- Current secret: ${WEBFLOW_CURRENT_SECRET.substring(0, 10)}...`);
console.log('Webhook routes are being registered...');
console.log('-------------------------');

// Debug endpoint - no authentication required
router.get('/debug', (req, res) => {
  console.log('Debug endpoint accessed');
  res.status(200).json({
    status: 'ok',
    message: 'Webhook module is functioning',
    routes: [
      '/api/webhooks/debug',
      '/api/webhooks/test',
      '/api/webhooks/guest-list-registration'
    ],
    timestamps: {
      server: new Date().toISOString(),
      uptime: process.uptime()
    }
  });
});

// Simple endpoint to receive test form submissions
router.post('/test', (req, res) => {
  console.log('Received test webhook:', req.body);
  res.status(200).json({
    success: true,
    message: 'Test webhook received successfully',
    data: req.body
  });
});

// Route for checking if the webhook endpoint is accessible
router.get('/test', (req, res) => {
  console.log('Test GET endpoint accessed');
  res.status(200).json({
    status: 'online',
    message: 'Webhook test endpoint is active and ready to receive data'
  });
});

/**
 * Authenticate Webflow webhook request - can be bypassed when needed
 */
function authenticateWebflow(req, res, next) {
  console.log('Authenticating webhook with headers:', JSON.stringify(req.headers));
  
  const webhookSecret = req.headers['x-webflow-webhook-secret'];
  const url = req.originalUrl;
  
  // Check if it's a Webflow form submission (look for specific Webflow headers)
  const isWebflowFormSubmission = req.headers['x-webflow-signature'] || 
                                 req.headers['x-webflow-timestamp'] ||
                                 (req.body && req.body.triggerType === 'form_submission');

  // Debug info
  console.log(`Secret received: ${webhookSecret ? webhookSecret.substring(0, 10) + '...' : 'none'}`);
  console.log(`Expected secrets: ${WEBFLOW_WEBHOOK_SECRET.substring(0, 10)}... or ${WEBFLOW_NEW_SECRET.substring(0, 10)}... or ${WEBFLOW_LATEST_SECRET.substring(0, 10)}... or ${WEBFLOW_CURRENT_SECRET.substring(0, 10)}...`);
  console.log(`Is Webflow form submission: ${isWebflowFormSubmission}`);
  
  // If it's a Webflow form submission, allow it without authentication
  if (isWebflowFormSubmission) {
    console.log('Bypassing authentication for Webflow form submission');
    return next();
  }
  
  // Check against all four secrets
  if (webhookSecret !== WEBFLOW_WEBHOOK_SECRET && 
      webhookSecret !== WEBFLOW_NEW_SECRET && 
      webhookSecret !== WEBFLOW_LATEST_SECRET &&
      webhookSecret !== WEBFLOW_CURRENT_SECRET) {
    console.error('Invalid webhook secret:', webhookSecret ? webhookSecret.substring(0, 10) + '...' : 'none');
    console.error('Expected one of:', 
      WEBFLOW_WEBHOOK_SECRET.substring(0, 10) + '...', 'or', 
      WEBFLOW_NEW_SECRET.substring(0, 10) + '...', 'or',
      WEBFLOW_LATEST_SECRET.substring(0, 10) + '...', 'or',
      WEBFLOW_CURRENT_SECRET.substring(0, 10) + '...');
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  console.log('Webhook authentication successful');
  next();
}

/**
 * Add or update contact in Mailchimp with proper workflow
 */
async function addToMailchimp(guestData, eventName) {
  try {
    console.log('Starting Mailchimp integration for:', guestData.email);
    console.log('MAILCHIMP_SERVER value:', MAILCHIMP_SERVER);
    console.log('MAILCHIMP_API_KEY value:', MAILCHIMP_API_KEY ? MAILCHIMP_API_KEY.substring(0, 10) + '...' : 'undefined');
    console.log('MAILCHIMP_LIST_ID value:', MAILCHIMP_LIST_ID);
    
    // Create subscriber hash for checking existing subscriber
    const crypto = require('crypto');
    const subscriberHash = crypto.createHash('md5').update(guestData.email.toLowerCase()).digest('hex');
    
    const baseUrl = `https://${MAILCHIMP_SERVER}.api.mailchimp.com/3.0/lists/${MAILCHIMP_LIST_ID}`;
    console.log('Constructed baseUrl:', baseUrl);
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Basic ${Buffer.from(`apikey:${MAILCHIMP_API_KEY}`).toString('base64')}`
    };
    
    // Prepare merge fields including DOB and event details
    // Using both standard Mailchimp fields and custom fields for the email template
    const eventDate = guestData.event_date ? new Date(guestData.event_date).toLocaleDateString('en-AU', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }) : 'TBA';
    
    const mergeFields = {
      FNAME: guestData.first_name,
      LNAME: guestData.last_name,
      EVENTNAME: eventName,
      EVENTDATE: eventDate,
      // Also add alternative field names that might be used in the template
      'First Name': guestData.first_name,
      'Last Name': guestData.last_name,
      // Add more variations that might be used in email templates
      FIRSTNAME: guestData.first_name,
      LASTNAME: guestData.last_name,
      EVENT_NAME: eventName,
      EVENT_DATE: eventDate
    };
    
    // Add DOB if available (format as MM/DD/YYYY for Mailchimp)
    if (guestData.dob) {
      try {
        const dobDate = new Date(guestData.dob);
        if (!isNaN(dobDate.getTime())) {
          const month = String(dobDate.getMonth() + 1).padStart(2, '0');
          const day = String(dobDate.getDate()).padStart(2, '0');
          const year = dobDate.getFullYear();
          
          // Add multiple DOB formats for template compatibility
          mergeFields.BIRTHDAY = `${month}/${day}/${year}`;
          mergeFields.DOB = `${month}/${day}/${year}`;
          mergeFields.DATEOFBIRTH = `${month}/${day}/${year}`;
          mergeFields['Date of Birth'] = `${month}/${day}/${year}`;
          
          console.log(`DOB formatted for Mailchimp: ${mergeFields.BIRTHDAY}`);
        }
      } catch (dobError) {
        console.log('DOB parsing error, skipping:', dobError.message);
      }
    } else {
      console.log('No DOB provided for guest');
    }
    
    console.log('Merge fields prepared:', mergeFields);
    
    // Step 1: Use PUT method for upsert (add or update)
    const subscriberData = {
      email_address: guestData.email,
      status_if_new: 'subscribed',
      merge_fields: mergeFields
    };
    
    console.log('Using PUT method for upsert (add or update subscriber)...');
    console.log('Subscriber data:', JSON.stringify(subscriberData, null, 2));
    
    const memberResponse = await axios.put(`${baseUrl}/members/${subscriberHash}`, subscriberData, { headers });
    console.log('Subscriber upsert successful:', memberResponse.data.email_address);
    
    // Determine if it was an update or new creation
    const isExistingSubscriber = memberResponse.data.timestamp_opt ? true : false;
    if (isExistingSubscriber) {
      console.log('Existing subscriber updated successfully');
    } else {
      console.log('New subscriber created successfully');
    }
    
    // Step 3: Add event tag
    const eventTag = eventName.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '_').toUpperCase();
    console.log('Adding event tag:', eventTag);
    
    await axios.post(`${baseUrl}/members/${subscriberHash}/tags`, {
      tags: [
        { name: eventTag, status: 'active' }
      ]
    }, { headers });
    
    // Step 4: Add GUESTLISTSUCCESS tag to trigger confirmation email
    // Always add the tag, even for existing subscribers - this ensures every registration gets a confirmation
    console.log('Adding GUESTLISTSUCCESS tag for automation trigger');
    
    // Add only the standard tag for automation (no unique timestamps needed)
    const tagResponse = await axios.post(`${baseUrl}/members/${subscriberHash}/tags`, {
      tags: [
        { name: 'GUESTLISTSUCCESS', status: 'active' }
      ]
    }, { headers });
    console.log('GUESTLISTSUCCESS tag added successfully, response status:', tagResponse.status);
    
    // Step 5: Wait 15 seconds then remove the tag 
    // Quick removal to allow re-triggering for subsequent event registrations
    setTimeout(async () => {
      try {
        console.log('Removing GUESTLISTSUCCESS tag after 15 seconds...');
        await axios.post(`${baseUrl}/members/${subscriberHash}/tags`, {
          tags: [
            { name: 'GUESTLISTSUCCESS', status: 'inactive' }
          ]
        }, { headers });
        console.log('GUESTLISTSUCCESS tag removed successfully - ready for next event registration');
      } catch (removeError) {
        console.error('Error removing GUESTLISTSUCCESS tag:', removeError.response?.data || removeError.message);
        // Don't fail the whole process if tag removal fails
      }
    }, 15000); // 15 seconds = 15,000ms
    
    console.log('Mailchimp integration completed successfully');
    return true;
    
  } catch (error) {
    console.error('Error in Mailchimp integration:', error.response?.data || error.message);
    return false;
  }
}

// Allow unhandled errors to be caught rather than crashing the app
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

/**
 * Main webhook endpoint for Webflow form submissions
 */
router.post('/guest-list-registration', authenticateWebflow, async (req, res) => {
  try {
    console.log('Received webhook from Webflow:', req.body);
    
    // Extract data from Webflow submission
    let formData = req.body.data || req.body;
    
    // Check if this is a Webflow form submission with triggerType
    if (req.body.triggerType === 'form_submission' && req.body.payload) {
      console.log('Processing Webflow form submission with triggerType');
      formData = req.body.payload.data || {};
      
      // Get the date field
      let dobValue = formData['data-date'] || formData['dob'] || null;
      
      // Convert date from DD/MM/YYYY to YYYY-MM-DD if needed
      if (dobValue && typeof dobValue === 'string') {
        // Check if it's in DD/MM/YYYY format
        if (dobValue.match(/^\d{2}\/\d{2}\/\d{4}$/)) {
          const [day, month, year] = dobValue.split('/');
          dobValue = `${year}-${month}-${day}`;
        }
        // If already in YYYY-MM-DD format, keep as is
      }
      
      // Create a standardized object from Webflow's hyphenated field names
      const mappedData = {
        event_name: formData['event-name'] || formData['event_name'] || 'Upcoming Event',
        event_date: formData['event-date'] || formData['event_date'] || new Date().toISOString().split('T')[0],
        first_name: formData['first-name'] || formData['first_name'] || '',
        last_name: formData['last-name'] || formData['last_name'] || '',
        email: formData['data-email'] || formData['email'] || '',
        dob: dobValue
      };
      
      // Use the mapped data
      formData = mappedData;
    }
    
    console.log('Processed form data:', formData);
    
    if (!formData) {
      console.error('No form data found in request');
      return res.status(400).json({ 
        success: false, 
        message: 'No form data found in request'
      });
    }
    
    // Find existing event (DO NOT CREATE - API-only system)
    const eventName = formData.event_name || 'Upcoming Event';
    
    let event = await Event.findOne({
      where: { name: eventName }
    });
    
    if (!event) {
      console.error('Event not found:', eventName);
      return res.status(400).json({ 
        success: false, 
        message: `Event "${eventName}" not found. Events must be created via Muzeek API first.`
      });
    }
    
    console.log('Found existing event:', event.name);
    
    // If DOB is null or invalid, set it to NULL for the database
    let dob = formData.dob;
    if (!dob || dob === 'Invalid date') {
      dob = null;
    }
    
    // Create guest record (allow duplicates - each registration is separate)
    const guest = await Guest.create({
      event_id: event.id,
      first_name: formData.first_name,
      last_name: formData.last_name,
      email: formData.email,
      dob: dob,
      checked_in: false
    });
    
    console.log('Guest added successfully:', guest.id);
    
    // Add a small delay to ensure separate processing for rapid duplicate registrations
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Add to Mailchimp in background with full event details
    const eventDetails = {
      ...guest.dataValues,
      event_name: event.name,
      event_date: event.event_date || formData.event_date
    };
    
    console.log('Event details being sent to Mailchimp:', eventDetails);
    console.log('Event date from database:', event.event_date);
    console.log('Event date from form:', formData.event_date);
    
    addToMailchimp(eventDetails, event.name)
      .then(success => {
        console.log('Mailchimp integration completed:', success ? 'Success' : 'Failed');
      })
      .catch(err => {
        console.error('Mailchimp integration error:', err);
      });
    
    // Respond to Webflow
    res.status(200).json({
      success: true,
      message: 'Guest registration successful',
      data: {
        guest_id: guest.id,
        event_id: event.id
      }
    });
  } catch (error) {
    console.error('Error processing webhook:', error);
    res.status(500).json({
      success: false,
      message: 'Error processing guest registration',
      error: error.message
    });
  }
});

// Route for checking if the webhook endpoint is accessible
router.get('/guest-list-registration', (req, res) => {
  console.log('Guest list registration GET endpoint accessed');
  res.status(200).json({
    status: 'online',
    message: 'Webhook endpoint is active and ready to receive data'
  });
});

// Webhook fallback for handling other HTTP methods
router.all('/*', (req, res) => {
  console.log(`Unhandled webhook request: ${req.method} ${req.path}`);
  res.status(200).json({
    message: 'Webhook received but no specific handler available',
    method: req.method,
    path: req.path
  });
});

console.log('All webhook routes registered successfully');
module.exports = router; 