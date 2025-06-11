// Guest History API Routes
const express = require('express');
const router = express.Router();
const guestHistoryService = require('../services/guestHistoryService');

/**
 * GET /api/guest-history/:email
 * Get full event history for a specific guest
 */
router.get('/:email', async (req, res) => {
  try {
    const { email } = req.params;
    
    if (!email || !email.includes('@')) {
      return res.status(400).json({
        success: false,
        message: 'Valid email address required'
      });
    }
    
    console.log(`[API] Getting guest history for: ${email}`);
    
    const history = await guestHistoryService.getGuestHistory(email);
    
    if (!history) {
      return res.status(404).json({
        success: false,
        message: 'Guest not found in Mailchimp',
        data: {
          email,
          eventCount: 0,
          events: [],
          isReturningGuest: false
        }
      });
    }
    
    res.json({
      success: true,
      message: `Found ${history.eventCount} events for ${email}`,
      data: {
        email: history.email,
        eventCount: history.eventCount,
        events: history.events,
        memberSince: history.memberSince,
        isReturningGuest: history.eventCount > 0,
        status: history.status
      }
    });
    
  } catch (error) {
    console.error('[API] Error getting guest history:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching guest history',
      error: error.message
    });
  }
});

/**
 * GET /api/guest-history/:email/summary
 * Get basic summary for a guest (just count and basic info)
 */
router.get('/:email/summary', async (req, res) => {
  try {
    const { email } = req.params;
    
    if (!email || !email.includes('@')) {
      return res.status(400).json({
        success: false,
        message: 'Valid email address required'
      });
    }
    
    console.log(`[API] Getting guest summary for: ${email}`);
    
    const summary = await guestHistoryService.getGuestHistorySummary(email);
    
    if (!summary) {
      return res.json({
        success: true,
        message: 'Guest not found - first time visitor',
        data: {
          email,
          eventCount: 0,
          isReturningGuest: false,
          memberSince: null
        }
      });
    }
    
    res.json({
      success: true,
      message: `Guest has attended ${summary.eventCount} events`,
      data: summary
    });
    
  } catch (error) {
    console.error('[API] Error getting guest summary:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching guest summary',
      error: error.message
    });
  }
});

/**
 * POST /api/guest-history/batch
 * Get summaries for multiple guests
 * Body: { emails: ["email1@example.com", "email2@example.com"] }
 */
router.post('/batch', async (req, res) => {
  try {
    const { emails } = req.body;
    
    if (!emails || !Array.isArray(emails) || emails.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Array of email addresses required'
      });
    }
    
    // Validate emails
    const validEmails = emails.filter(email => email && email.includes('@'));
    
    if (validEmails.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'No valid email addresses provided'
      });
    }
    
    console.log(`[API] Getting batch guest histories for ${validEmails.length} emails`);
    
    const histories = await guestHistoryService.batchGetGuestHistories(validEmails);
    
    res.json({
      success: true,
      message: `Processed ${validEmails.length} guests`,
      data: histories
    });
    
  } catch (error) {
    console.error('[API] Error getting batch guest histories:', error);
    res.status(500).json({
      success: false,
      message: 'Error fetching batch guest histories',
      error: error.message
    });
  }
});

module.exports = router; 