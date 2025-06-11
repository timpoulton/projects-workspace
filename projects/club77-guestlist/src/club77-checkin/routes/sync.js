const express = require('express');
const router = express.Router();
const { Event } = require('../models');
const MuzeekService = require('../services/muzeek');

// Sync events from Muzeek
router.post('/muzeek/events', async (req, res) => {
  try {
    console.log('Starting Muzeek events sync...');
    
    const muzeekService = new MuzeekService();
    const syncResult = await muzeekService.syncEvents();
    
    if (!syncResult.success) {
      return res.status(500).json({
        success: false,
        message: 'Failed to sync with Muzeek',
        error: syncResult.error
      });
    }
    
    // Update or create events in database
    let created = 0;
    let updated = 0;
    let errors = [];
    
    for (const eventData of syncResult.events) {
      try {
        // Check if event already exists
        const existingEvent = await Event.findOne({
          where: { muzeek_id: eventData.muzeek_id }
        });
        
        if (existingEvent) {
          // Update existing event
          await existingEvent.update(eventData);
          updated++;
          console.log(`Updated event: ${eventData.name}`);
        } else {
          // Create new event
          await Event.create(eventData);
          created++;
          console.log(`Created new event: ${eventData.name}`);
        }
      } catch (error) {
        console.error(`Error saving event ${eventData.name}:`, error.message);
        errors.push({
          event: eventData.name,
          error: error.message
        });
      }
    }
    
    console.log(`Sync complete: ${created} created, ${updated} updated, ${errors.length} errors`);
    
    res.json({
      success: true,
      message: 'Muzeek sync completed',
      stats: {
        total: syncResult.events.length,
        created,
        updated,
        errors: errors.length
      },
      errors: errors.length > 0 ? errors : undefined
    });
    
  } catch (error) {
    console.error('Error in Muzeek sync route:', error.message);
    res.status(500).json({
      success: false,
      message: 'Internal server error during sync',
      error: error.message
    });
  }
});

// Get sync status
router.get('/muzeek/status', async (req, res) => {
  try {
    const events = await Event.findAll({
      where: {
        muzeek_id: { [require('sequelize').Op.not]: null }
      },
      order: [['last_synced', 'DESC']]
    });
    
    const lastSync = events.length > 0 ? events[0].last_synced : null;
    const muzeekEvents = events.length;
    const liveEvents = events.filter(e => e.is_live && e.muzeek_published).length;
    
    res.json({
      success: true,
      status: {
        lastSync,
        totalMuzeekEvents: muzeekEvents,
        liveEvents,
        needsSync: !lastSync || (new Date() - new Date(lastSync)) > 3600000 // 1 hour
      }
    });
    
  } catch (error) {
    console.error('Error getting sync status:', error.message);
    res.status(500).json({
      success: false,
      message: 'Error getting sync status',
      error: error.message
    });
  }
});

// Test Muzeek connection
router.get('/muzeek/test', async (req, res) => {
  try {
    const muzeekService = new MuzeekService();
    const testResult = await muzeekService.testConnection();
    
    res.json(testResult);
    
  } catch (error) {
    console.error('Error testing Muzeek connection:', error.message);
    res.status(500).json({
      success: false,
      message: 'Muzeek connection failed',
      error: error.message
    });
  }
});

// Legacy Webflow endpoints (redirect to Muzeek)
router.post('/webflow/events', async (req, res) => {
  console.log('Legacy Webflow endpoint called, redirecting to Muzeek...');
  req.url = '/muzeek/events';
  return router.handle(req, res);
});

router.get('/webflow/status', async (req, res) => {
  console.log('Legacy Webflow endpoint called, redirecting to Muzeek...');
  req.url = '/muzeek/status';
  return router.handle(req, res);
});

router.get('/webflow/test', async (req, res) => {
  console.log('Legacy Webflow endpoint called, redirecting to Muzeek...');
  req.url = '/muzeek/test';
  return router.handle(req, res);
});

// Test Mailchimp integration
router.get('/mailchimp/test', async (req, res) => {
  try {
    const axios = require('axios');
    
    const MAILCHIMP_API_KEY = process.env.MAILCHIMP_API_KEY || '2692c472af4f17326f5c1384a61b4c5b-us12';
    const MAILCHIMP_SERVER = process.env.MAILCHIMP_SERVER || 'us12';
    const MAILCHIMP_LIST_ID = process.env.MAILCHIMP_LIST_ID || '53f56e2c77';
    
    const baseUrl = `https://${MAILCHIMP_SERVER}.api.mailchimp.com/3.0/lists/${MAILCHIMP_LIST_ID}`;
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Basic ${Buffer.from(`apikey:${MAILCHIMP_API_KEY}`).toString('base64')}`
    };
    
    // Test API connection
    const listResponse = await axios.get(baseUrl, { headers });
    
    res.json({
      success: true,
      message: 'Mailchimp API connection successful',
      list: {
        id: listResponse.data.id,
        name: listResponse.data.name,
        member_count: listResponse.data.stats.member_count
      },
      config: {
        server: MAILCHIMP_SERVER,
        list_id: MAILCHIMP_LIST_ID,
        api_key_prefix: MAILCHIMP_API_KEY ? MAILCHIMP_API_KEY.substring(0, 10) + '...' : 'undefined'
      }
    });
    
  } catch (error) {
    console.error('Mailchimp test error:', error.response?.data || error.message);
    res.status(500).json({
      success: false,
      message: 'Mailchimp API test failed',
      error: error.response?.data || error.message
    });
  }
});

module.exports = router; 