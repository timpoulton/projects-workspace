const express = require('express');
const router = express.Router();
const { Event, Guest } = require('../models');

// Get a specific event and its guests
router.get('/:id', async (req, res) => {
  try {
    const eventId = req.params.id;
    
    // Get the current event
    const currentEvent = await Event.findByPk(eventId);
    
    if (!currentEvent) {
      req.flash('error_msg', 'Event not found');
      return res.redirect('/');
    }
    
    // Get all events for the dropdown
    const events = await Event.findAll({
      order: [['event_date', 'DESC']]
    });
    
    // Get all guests for this event
    const guests = await Guest.findAll({
      where: { event_id: eventId },
      order: [['last_name', 'ASC'], ['first_name', 'ASC']]
    });
    
    // Calculate stats
    const total = guests.length;
    const checkedIn = guests.filter(guest => guest.checked_in).length;
    const percentage = total > 0 ? Math.round((checkedIn / total) * 100) : 0;
    
    res.render('event', {
      title: `${currentEvent.name} - Club77 Check-In`,
      events,
      currentEvent,
      guests,
      filter: req.query.filter || 'all',
      stats: {
        total,
        checkedIn,
        percentage
      },
      layout: false
    });
  } catch (error) {
    console.error('Error fetching event:', error);
    req.flash('error_msg', 'Error loading event data');
    res.redirect('/');
  }
});

// Get filtered guests for an event (AJAX endpoint)
router.get('/:id/guests', async (req, res) => {
  try {
    const eventId = req.params.id;
    const filter = req.query.filter || 'all';
    
    // Build the query based on the filter
    const query = {
      where: { event_id: eventId },
      order: [['last_name', 'ASC'], ['first_name', 'ASC']]
    };
    
    // Apply filter if not 'all'
    if (filter === 'checked-in') {
      query.where.checked_in = true;
    } else if (filter === 'not-checked-in') {
      query.where.checked_in = false;
    }
    
    // Get filtered guests
    const guests = await Guest.findAll(query);
    
    // Calculate stats
    const total = guests.length;
    const checkedIn = guests.filter(guest => guest.checked_in).length;
    const percentage = total > 0 ? Math.round((checkedIn / total) * 100) : 0;
    
    // If this is an AJAX request, return JSON
    if (req.xhr) {
      return res.json({
        guests,
        stats: {
          total,
          checkedIn,
          percentage
        }
      });
    }
    
    // Otherwise redirect to the event page
    res.redirect(`/events/${eventId}?filter=${filter}`);
  } catch (error) {
    console.error('Error filtering guests:', error);
    if (req.xhr) {
      return res.status(500).json({ error: 'Error filtering guests' });
    }
    req.flash('error_msg', 'Error filtering guests');
    res.redirect(`/events/${req.params.id}`);
  }
});

// Export routes
module.exports = router; 