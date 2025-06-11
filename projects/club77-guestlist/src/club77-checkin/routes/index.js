const express = require('express');
const router = express.Router();
const { Event, Guest } = require('../models');
const { Op } = require('sequelize');
const MuzeekService = require('../services/muzeek');

// Home page - show all events for selection
router.get('/', async (req, res) => {
  try {
    // Get all events and sort by date (earliest first)
    // Only show live/published events
    const events = await Event.findAll({
      where: {
        is_live: true
      },
      order: [['event_date', 'ASC']]
    });
    
    // Check if we need to sync with Muzeek (if no events or last sync > 1 hour ago)
    const needsSync = events.length === 0 || 
      events.every(e => !e.last_synced || (new Date() - new Date(e.last_synced)) > 3600000);
    
    // Always render the homepage with events list
    res.render('index', { 
      title: 'Club77 Check-In System',
      events: events,
      currentEvent: null,
      guests: [],
      needsSync,
      stats: {
        total: 0,
        checkedIn: 0,
        percentage: 0
      },
      layout: false
    });
  } catch (error) {
    console.error('Error fetching data:', error);
    req.flash('error_msg', 'Error loading events');
    res.render('index', { 
      title: 'Club77 Check-In System',
      events: [],
      currentEvent: null,
      guests: [],
      needsSync: true,
      stats: {
        total: 0,
        checkedIn: 0,
        percentage: 0
      },
      layout: false
    });
  }
});

// Search route
router.get('/search', async (req, res) => {
  try {
    const { q, event_id } = req.query;
    
    if (!q) {
      return res.redirect(event_id ? `/events/${event_id}` : '/');
    }
    
    // Build the search query
    const searchQuery = {
      where: {
        [Op.or]: [
          { first_name: { [Op.like]: `%${q}%` } },
          { last_name: { [Op.like]: `%${q}%` } },
          { email: { [Op.like]: `%${q}%` } }
        ]
      },
      include: [{
        model: Event,
        as: 'event'
      }],
      order: [['last_name', 'ASC'], ['first_name', 'ASC']]
    };
    
    // If event_id is provided, filter by that event
    if (event_id) {
      searchQuery.where.event_id = event_id;
    }
    
    // Get guests matching the search query
    const guests = await Guest.findAll(searchQuery);
    
    // Get all events for the dropdown
    const events = await Event.findAll({
      order: [['event_date', 'ASC']]
    });
    
    // Get current event if event_id provided
    let currentEvent = null;
    if (event_id) {
      currentEvent = await Event.findByPk(event_id);
    }
    
    // Calculate stats for the search results
    const total = guests.length;
    const checkedIn = guests.filter(guest => guest.checked_in).length;
    const percentage = total > 0 ? Math.round((checkedIn / total) * 100) : 0;
    
    res.render('search', {
      title: `Search Results for "${q}" - Club77 Check-In`,
      events,
      currentEvent,
      guests,
      searchQuery: q,
      stats: {
        total,
        checkedIn,
        percentage
      }
    });
  } catch (error) {
    console.error('Error searching:', error);
    req.flash('error_msg', 'Error performing search');
    res.redirect('/');
  }
});

// Login page
router.get('/login', (req, res) => {
  res.render('login', { title: 'Login - Club77 Check-In' });
});

// Export routes
module.exports = router; 