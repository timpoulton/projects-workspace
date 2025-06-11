/**
 * Club77 Check-In System - Client-side JavaScript
 * Enhanced for real-time staff operations and mobile-first experience
 */

$(document).ready(function() {
  // Variables to store guest data for modals
  let selectedGuestId = null;
  let selectedGuestName = null;

  // Auto-refresh settings
  let autoRefreshInterval = null;
  let lastGuestCount = 0;
  
  // Mobile-specific settings
  let isMobile = window.innerWidth <= 768;
  let isTouch = 'ontouchstart' in window;
  
  // Initialize mobile optimizations
  initMobileOptimizations();
  
  // Initialize auto-refresh for real-time updates
  initAutoRefresh();

  // Mobile-optimized event handlers
  function initMobileOptimizations() {
    // Add touch feedback to buttons
    if (isTouch) {
      $(document).on('touchstart', '.btn', function() {
        $(this).addClass('btn-pressed');
      });
      
      $(document).on('touchend touchcancel', '.btn', function() {
        const $btn = $(this);
        setTimeout(() => $btn.removeClass('btn-pressed'), 150);
      });
      
      // Prevent double-tap zoom on buttons
      $(document).on('touchend', '.btn', function(e) {
        e.preventDefault();
        $(this).trigger('click');
      });
    }
    
    // Optimize table scrolling for mobile
    if (isMobile) {
      $('.table-responsive').css({
        '-webkit-overflow-scrolling': 'touch',
        'overflow-x': 'auto'
      });
    }
    
    // Add haptic feedback for supported devices
    if ('vibrate' in navigator) {
      $(document).on('click', '.btn-success, .btn-danger', function() {
        navigator.vibrate(50); // Short vibration for feedback
      });
    }
  }

  // Enhanced check-in button click handler with mobile optimizations
  $(document).on('click touchend', '.check-in-btn', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    selectedGuestId = $(this).data('guest-id');
    
    // Get the guest name from the row
    const $row = $(this).closest('tr');
    selectedGuestName = $row.find('td:first-child .fw-semibold').text() || $row.find('td:first-child').text();
    
    // Set the guest name in the modal
    $('#guest-name').text(selectedGuestName);
    
    // Show the modal with mobile-optimized settings
    const checkInModal = new bootstrap.Modal(document.getElementById('checkInModal'), {
      backdrop: 'static',
      keyboard: true
    });
    checkInModal.show();
    
    // Auto-focus confirm button on desktop, skip on mobile to prevent keyboard
    if (!isMobile) {
      setTimeout(() => $('#confirm-check-in').focus(), 300);
    }
  });

  // Enhanced confirm check-in with loading state
  $('#confirm-check-in').on('click', function() {
    if (!selectedGuestId) return;
    
    const $btn = $(this);
    const originalText = $btn.html();
    
    // Show loading state
    $btn.html('<i class="fas fa-spinner fa-spin me-1"></i> Checking In...').prop('disabled', true);
    
    // Send AJAX request to check in the guest
    $.ajax({
      url: `/guests/${selectedGuestId}/check-in`,
      method: 'POST',
      timeout: 10000, // 10 second timeout for mobile networks
      success: function(response) {
        if (response.success) {
          // Close the modal
          $('#checkInModal').modal('hide');
          
          // Update the UI
          updateGuestRow(selectedGuestId, true);
          
          // Show success message with mobile-friendly styling
          showAlert('success', `${selectedGuestName} checked in successfully`, true);
          
          // Update stats
          updateStats();
          
          // Haptic feedback for success
          if ('vibrate' in navigator) {
            navigator.vibrate([100, 50, 100]);
          }
        } else {
          // Show error message
          showAlert('danger', response.message || 'Error checking in guest');
        }
      },
      error: function(xhr, status, error) {
        let errorMsg = 'Error checking in guest. Please try again.';
        if (status === 'timeout') {
          errorMsg = 'Request timed out. Please check your connection and try again.';
        }
        showAlert('danger', errorMsg);
      },
      complete: function() {
        // Reset button state
        $btn.html(originalText).prop('disabled', false);
      }
    });
  });

  // Enhanced check-out button click handler
  $(document).on('click touchend', '.check-out-btn', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    selectedGuestId = $(this).data('guest-id');
    
    // Get the guest name from the row
    const $row = $(this).closest('tr');
    selectedGuestName = $row.find('td:first-child .fw-semibold').text() || $row.find('td:first-child').text();
    
    // Set the guest name in the modal
    $('#checkout-guest-name').text(selectedGuestName);
    
    // Show the modal
    const checkOutModal = new bootstrap.Modal(document.getElementById('checkOutModal'), {
      backdrop: 'static',
      keyboard: true
    });
    checkOutModal.show();
    
    // Auto-focus confirm button on desktop
    if (!isMobile) {
      setTimeout(() => $('#confirm-check-out').focus(), 300);
    }
  });

  // Enhanced confirm check-out with loading state
  $('#confirm-check-out').on('click', function() {
    if (!selectedGuestId) return;
    
    const $btn = $(this);
    const originalText = $btn.html();
    
    // Show loading state
    $btn.html('<i class="fas fa-spinner fa-spin me-1"></i> Checking Out...').prop('disabled', true);
    
    // Send AJAX request to check out the guest
    $.ajax({
      url: `/guests/${selectedGuestId}/check-out`,
      method: 'POST',
      timeout: 10000,
      success: function(response) {
        if (response.success) {
          // Close the modal
          $('#checkOutModal').modal('hide');
          
          // Update the UI
          updateGuestRow(selectedGuestId, false);
          
          // Show success message
          showAlert('success', `${selectedGuestName} checked out successfully`, true);
          
          // Update stats
          updateStats();
          
          // Haptic feedback
          if ('vibrate' in navigator) {
            navigator.vibrate([100, 50, 100]);
          }
        } else {
          // Show error message
          showAlert('danger', response.message || 'Error checking out guest');
        }
      },
      error: function(xhr, status, error) {
        let errorMsg = 'Error checking out guest. Please try again.';
        if (status === 'timeout') {
          errorMsg = 'Request timed out. Please check your connection and try again.';
        }
        showAlert('danger', errorMsg);
      },
      complete: function() {
        // Reset button state
        $btn.html(originalText).prop('disabled', false);
      }
    });
  });

  // Helper function to update a guest row after check-in/out
  function updateGuestRow(guestId, isCheckedIn) {
    const $row = $(`tr[data-guest-id="${guestId}"]`);
    
    if (isCheckedIn) {
      // Update row styling with animation
      $row.addClass('table-success');
      
      // Update status cell
      const currentTime = new Date().toLocaleTimeString();
      $row.find('td:nth-child(4)').html(
        `<span class="badge bg-success">
           <i class="fas fa-check me-1"></i>
           Checked In
         </span>
         <small class="text-muted d-block">${currentTime}</small>`
      );
      
      // Update action button
      $row.find('td:last-child').html(
        `<button class="btn btn-sm btn-outline-danger check-out-btn" 
                 data-guest-id="${guestId}"
                 title="Check out">
           <i class="fas fa-sign-out-alt me-1"></i>
           Check Out
         </button>`
      );
      
      // Update name cell to show arrival time
      const $nameCell = $row.find('td:first-child');
      if (!$nameCell.find('.text-success').length) {
        $nameCell.find('div').append(`
          <small class="text-success">
            <i class="fas fa-clock me-1"></i>
            Arrived: ${currentTime}
          </small>
        `);
      }
    } else {
      // Update row styling
      $row.removeClass('table-success');
      
      // Update status cell
      $row.find('td:nth-child(4)').html(
        `<span class="badge bg-danger">
           <i class="fas fa-clock me-1"></i>
           Pending Arrival
         </span>`
      );
      
      // Update action button
      $row.find('td:last-child').html(
        `<button class="btn btn-sm btn-success check-in-btn" 
                 data-guest-id="${guestId}"
                 title="Check in">
           <i class="fas fa-sign-in-alt me-1"></i>
           Check In
         </button>`
      );
      
      // Remove arrival time from name cell
      $row.find('td:first-child .text-success').remove();
    }
    
    // Add visual feedback animation
    $row.addClass('row-updated');
    setTimeout(() => $row.removeClass('row-updated'), 1000);
  }

  // Helper function to update stats
  function updateStats() {
    // Count total guests
    const total = $('#guests-table tbody tr').length;
    
    // Count checked-in guests
    const checkedIn = $('#guests-table tbody tr.table-success').length;
    
    // Calculate percentage
    const percentage = total > 0 ? Math.round((checkedIn / total) * 100) : 0;
    
    // Update the stats badges with animation
    $('.stats .badge').addClass('badge-updating');
    setTimeout(() => {
      $('.stats .badge.bg-primary').html(`<i class="fas fa-users me-1"></i> Total: ${total}`);
      $('.stats .badge.bg-success').html(`<i class="fas fa-check me-1"></i> Checked In: ${checkedIn}`);
      $('.stats .badge.bg-info').html(`<i class="fas fa-percentage me-1"></i> ${percentage}%`);
      $('.stats .badge').removeClass('badge-updating');
    }, 200);
  }

  // Enhanced alert function with mobile optimizations
  function showAlert(type, message, autoHide = true) {
    const alertId = 'alert-' + Date.now();
    const alertHTML = `
      <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show mobile-alert">
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `;
    
    // Add the alert at the top of the container
    $('.container').prepend(alertHTML);
    
    // Auto-hide after appropriate time for mobile
    if (autoHide) {
      const hideTime = isMobile ? 4000 : 3000; // Longer on mobile for readability
      setTimeout(function() {
        $(`#${alertId}`).alert('close');
      }, hideTime);
    }
    
    // Scroll to top on mobile to ensure alert is visible
    if (isMobile) {
      $('html, body').animate({ scrollTop: 0 }, 300);
    }
  }
  
  // Auto-refresh functionality optimized for mobile
  function initAutoRefresh() {
    // Get current event ID from URL
    const currentEventId = window.location.pathname.split('/')[2];
    if (!currentEventId) return;
    
    // Set initial guest count
    lastGuestCount = $('#guests-table tbody tr').length;
    
    // Adjust refresh interval based on device
    const refreshInterval = isMobile ? 15000 : 10000; // Longer on mobile to save battery
    
    // Start auto-refresh
    autoRefreshInterval = setInterval(function() {
      refreshGuestList(currentEventId);
    }, refreshInterval);
    
    // Add visual indicator for auto-refresh
    addAutoRefreshIndicator();
    
    // Pause auto-refresh when page is not visible (mobile battery optimization)
    document.addEventListener('visibilitychange', function() {
      if (document.hidden) {
        if (autoRefreshInterval) {
          clearInterval(autoRefreshInterval);
          autoRefreshInterval = null;
        }
      } else {
        if (!autoRefreshInterval) {
          autoRefreshInterval = setInterval(function() {
            refreshGuestList(currentEventId);
          }, refreshInterval);
        }
      }
    });
  }
  
  // Enhanced refresh function with better error handling
  function refreshGuestList(eventId) {
    const currentFilter = new URLSearchParams(window.location.search).get('filter') || 'all';
    
    $.ajax({
      url: `/events/${eventId}/guests?filter=${currentFilter}`,
      method: 'GET',
      timeout: 8000, // Shorter timeout for auto-refresh
      success: function(response) {
        if (response.guests) {
          updateGuestTable(response.guests);
          updateStatsDisplay(response.stats);
          
          // Check for new registrations
          if (response.guests.length > lastGuestCount) {
            const newGuests = response.guests.length - lastGuestCount;
            showAlert('info', `${newGuests} new guest${newGuests > 1 ? 's' : ''} registered!`, true);
            
            // Flash the new guest indicator
            flashNewGuestIndicator();
            
            // Haptic feedback for new guests
            if ('vibrate' in navigator) {
              navigator.vibrate([200, 100, 200]);
            }
          }
          
          lastGuestCount = response.guests.length;
          
          // Update refresh indicator
          updateRefreshIndicator('success');
        }
      },
      error: function(xhr, status, error) {
        console.log('Auto-refresh failed:', status, error);
        updateRefreshIndicator('error');
        
        // Show error only if it's a persistent issue
        if (status !== 'timeout') {
          showAlert('danger', 'Connection issue. Retrying...', true);
        }
      }
    });
  }
  
  // Update the guest table with new data and mobile optimizations
  function updateGuestTable(guests) {
    const $tbody = $('#guests-table tbody');
    $tbody.empty();
    
    if (guests.length > 0) {
      guests.forEach(guest => {
        const dobDisplay = guest.dob ? new Date(guest.dob).toLocaleDateString('en-AU') : 'N/A';
        const ageDisplay = guest.dob ? Math.floor((new Date() - new Date(guest.dob)) / (365.25 * 24 * 60 * 60 * 1000)) : '';
        const checkedInClass = guest.checked_in ? 'table-success' : '';
        
        const statusBadge = guest.checked_in ? 
          `<span class="badge bg-success">
             <i class="fas fa-check me-1"></i>
             Checked In
           </span>
           ${guest.check_in_time ? `<small class="text-muted d-block">${new Date(guest.check_in_time).toLocaleTimeString()}</small>` : ''}` :
          `<span class="badge bg-danger">
             <i class="fas fa-clock me-1"></i>
             Pending Arrival
           </span>`;
        
        const actionButton = guest.checked_in ?
          `<button class="btn btn-sm btn-outline-danger check-out-btn" 
                   data-guest-id="${guest.id}"
                   title="Check out ${guest.first_name} ${guest.last_name}">
             <i class="fas fa-sign-out-alt me-1"></i>
             Check Out
           </button>` :
          `<button class="btn btn-sm btn-success check-in-btn" 
                   data-guest-id="${guest.id}"
                   title="Check in ${guest.first_name} ${guest.last_name}">
             <i class="fas fa-sign-in-alt me-1"></i>
             Check In
           </button>`;
        
        const row = `
          <tr data-guest-id="${guest.id}" class="${checkedInClass}">
            <td>
              <div class="d-flex align-items-center">
                <div class="avatar-placeholder me-2">
                  <i class="fas fa-user-circle fa-2x text-muted"></i>
                </div>
                <div>
                  <div class="fw-semibold">${guest.first_name} ${guest.last_name}</div>
                  ${guest.checked_in && guest.check_in_time ? 
                    `<small class="text-success">
                       <i class="fas fa-clock me-1"></i>
                       Arrived: ${new Date(guest.check_in_time).toLocaleTimeString()}
                     </small>` : ''}
                </div>
              </div>
            </td>
            <td>
              ${guest.email ? 
                `<a href="mailto:${guest.email}" class="text-decoration-none">${guest.email}</a>` : 
                '<span class="text-muted">N/A</span>'}
            </td>
            <td>
              ${guest.dob ? 
                `${dobDisplay}${ageDisplay ? `<small class="text-muted d-block">Age: ${ageDisplay}</small>` : ''}` : 
                '<span class="text-muted">N/A</span>'}
            </td>
            <td>${statusBadge}</td>
            <td class="text-center">${actionButton}</td>
          </tr>
        `;
        
        $tbody.append(row);
      });
    } else {
      $tbody.append(`
        <tr>
          <td colspan="5" class="text-center py-5">
            <div class="empty-state">
              <i class="fas fa-users fa-3x text-muted mb-3"></i>
              <h5 class="text-muted">No guests found</h5>
              <p class="text-muted">
                ${$('.btn-group .btn.active').text().includes('All') ? 
                  'Guests will appear here as they register for this event.' : 
                  'Try changing the filter or check back later for new registrations.'}
              </p>
            </div>
          </td>
        </tr>
      `);
    }
  }
  
  // Update stats display with animation
  function updateStatsDisplay(stats) {
    $('.stats .badge').addClass('badge-updating');
    setTimeout(() => {
      $('.stats .badge.bg-primary').html(`<i class="fas fa-users me-1"></i> Total: ${stats.total}`);
      $('.stats .badge.bg-success').html(`<i class="fas fa-check me-1"></i> Checked In: ${stats.checkedIn}`);
      $('.stats .badge.bg-info').html(`<i class="fas fa-percentage me-1"></i> ${stats.percentage}%`);
      $('.stats .badge').removeClass('badge-updating');
    }, 200);
  }
  
  // Add auto-refresh indicator with mobile positioning
  function addAutoRefreshIndicator() {
    const position = isMobile ? 'bottom-0 start-50 translate-middle-x' : 'bottom-0 end-0';
    const indicator = `
      <div id="auto-refresh-indicator" class="position-fixed ${position} m-3">
        <span class="badge bg-secondary">
          <i class="fas fa-sync-alt me-1"></i> 
          <span class="d-none d-sm-inline">Auto-refresh: ON</span>
          <span class="d-sm-none">LIVE</span>
        </span>
      </div>
    `;
    $('body').append(indicator);
  }
  
  // Update refresh indicator status
  function updateRefreshIndicator(status) {
    const $indicator = $('#auto-refresh-indicator .badge');
    $indicator.removeClass('bg-secondary bg-success bg-danger');
    
    if (status === 'success') {
      $indicator.addClass('bg-success');
      setTimeout(() => $indicator.addClass('bg-secondary').removeClass('bg-success'), 1000);
    } else if (status === 'error') {
      $indicator.addClass('bg-danger');
      setTimeout(() => $indicator.addClass('bg-secondary').removeClass('bg-danger'), 2000);
    }
  }
  
  // Flash indicator for new guests
  function flashNewGuestIndicator() {
    $('#auto-refresh-indicator .badge').addClass('bg-info').removeClass('bg-secondary');
    setTimeout(function() {
      $('#auto-refresh-indicator .badge').addClass('bg-secondary').removeClass('bg-info');
    }, 2000);
  }
  
  // Manual refresh button with loading state
  $(document).on('click', '#manual-refresh', function() {
    const $btn = $(this);
    const originalHtml = $btn.html();
    
    $btn.html('<i class="fas fa-spinner fa-spin me-1"></i> <span class="d-none d-sm-inline">Refreshing...</span>')
        .prop('disabled', true);
    
    const currentEventId = window.location.pathname.split('/')[2];
    if (currentEventId) {
      refreshGuestList(currentEventId);
      showAlert('info', 'Guest list refreshed', true);
      
      setTimeout(() => {
        $btn.html(originalHtml).prop('disabled', false);
      }, 1000);
    }
  });
  
  // Handle orientation change on mobile
  $(window).on('orientationchange resize', function() {
    isMobile = window.innerWidth <= 768;
    
    // Adjust auto-refresh indicator position
    const $indicator = $('#auto-refresh-indicator');
    if (isMobile) {
      $indicator.removeClass('bottom-0 end-0').addClass('bottom-0 start-50 translate-middle-x');
    } else {
      $indicator.removeClass('bottom-0 start-50 translate-middle-x').addClass('bottom-0 end-0');
    }
  });
  
  // Cleanup on page unload
  $(window).on('beforeunload', function() {
    if (autoRefreshInterval) {
      clearInterval(autoRefreshInterval);
    }
  });
  
  // Add CSS for mobile enhancements
  $('<style>')
    .prop('type', 'text/css')
    .html(`
      .btn-pressed {
        transform: scale(0.95) !important;
        opacity: 0.8 !important;
      }
      
      .row-updated {
        animation: rowUpdate 1s ease-out;
      }
      
      .badge-updating {
        animation: badgeUpdate 0.3s ease-in-out;
      }
      
      .mobile-alert {
        font-size: 0.95rem;
        border-radius: 12px;
      }
      
      @keyframes rowUpdate {
        0% { background-color: rgba(255, 0, 199, 0.3); }
        100% { background-color: transparent; }
      }
      
      @keyframes badgeUpdate {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
      }
      
      /* Mobile-specific table optimizations */
      @media (max-width: 768px) {
        .table td {
          padding: 12px 8px;
          font-size: 0.85rem;
        }
        
        .table .btn-sm {
          padding: 8px 12px;
          font-size: 0.8rem;
        }
        
        .avatar-placeholder {
          width: 40px;
          height: 40px;
        }
        
        .avatar-placeholder i {
          font-size: 1.5rem;
        }
      }
    `)
    .appendTo('head');
}); 