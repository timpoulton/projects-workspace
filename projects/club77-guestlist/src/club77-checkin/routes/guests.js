const express = require('express');
const router = express.Router();
const { Guest } = require('../models');

// Check in a guest
router.post('/:id/check-in', async (req, res) => {
  try {
    const guestId = req.params.id;
    
    // Find the guest
    const guest = await Guest.findByPk(guestId);
    
    if (!guest) {
      if (req.xhr) {
        return res.status(404).json({ success: false, message: 'Guest not found' });
      }
      req.flash('error_msg', 'Guest not found');
      return res.redirect('back');
    }
    
    // Check in the guest (using the instance method defined in the model)
    await guest.checkIn();
    
    if (req.xhr) {
      return res.json({ 
        success: true, 
        message: `${guest.first_name} ${guest.last_name} checked in successfully`,
        guest
      });
    }
    
    req.flash('success_msg', `${guest.first_name} ${guest.last_name} checked in successfully`);
    res.redirect('back');
  } catch (error) {
    console.error('Error checking in guest:', error);
    if (req.xhr) {
      return res.status(500).json({ success: false, message: 'Error checking in guest' });
    }
    req.flash('error_msg', 'Error checking in guest');
    res.redirect('back');
  }
});

// Check out a guest
router.post('/:id/check-out', async (req, res) => {
  try {
    const guestId = req.params.id;
    
    // Find the guest
    const guest = await Guest.findByPk(guestId);
    
    if (!guest) {
      if (req.xhr) {
        return res.status(404).json({ success: false, message: 'Guest not found' });
      }
      req.flash('error_msg', 'Guest not found');
      return res.redirect('back');
    }
    
    // Check out the guest (using the instance method defined in the model)
    await guest.checkOut();
    
    if (req.xhr) {
      return res.json({ 
        success: true, 
        message: `${guest.first_name} ${guest.last_name} checked out successfully`,
        guest
      });
    }
    
    req.flash('success_msg', `${guest.first_name} ${guest.last_name} checked out successfully`);
    res.redirect('back');
  } catch (error) {
    console.error('Error checking out guest:', error);
    if (req.xhr) {
      return res.status(500).json({ success: false, message: 'Error checking out guest' });
    }
    req.flash('error_msg', 'Error checking out guest');
    res.redirect('back');
  }
});

// Get guest details (AJAX endpoint)
router.get('/:id', async (req, res) => {
  try {
    const guestId = req.params.id;
    
    // Find the guest with its event
    const guest = await Guest.findByPk(guestId, {
      include: ['event']
    });
    
    if (!guest) {
      return res.status(404).json({ success: false, message: 'Guest not found' });
    }
    
    res.json({ success: true, guest });
  } catch (error) {
    console.error('Error fetching guest details:', error);
    res.status(500).json({ success: false, message: 'Error fetching guest details' });
  }
});

// Export routes
module.exports = router; 