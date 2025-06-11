const axios = require('axios');

class MuzeekService {
  constructor() {
    this.apiToken = process.env.MUZEEK_API_TOKEN || 'mzku-MS03MTU2NTIxODUtYjI2ZjBlY2FkMDA2MjcwMDljYmI4OWU2NDA5ZjEyZDQ1ZGU2NzdiOQ';
    this.baseURL = 'https://muzeek.com/i/api';
    
    // Create axios client with proper headers for localhost/container requests
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'token': this.apiToken,
        'accept': 'application/json',
        'User-Agent': 'Club77-CheckinApp/1.0 (https://checkin.projekt-ai.net)',
        'Origin': 'https://checkin.projekt-ai.net',
        'Referer': 'https://checkin.projekt-ai.net/',
        'Host': 'muzeek.com',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
      },
      timeout: 30000 // 30 second timeout
    });
  }

  // Format date to DD-MM-YYYY as required by Muzeek API
  formatDateForAPI(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}-${month}-${year}`;
  }

  // Test API connection
  async testConnection() {
    try {
      console.log('=== MUZEEK API TEST DEBUG ===');
      console.log('Testing Muzeek API with token:', this.apiToken.substring(0, 10) + '...');
      console.log('Full token length:', this.apiToken.length);
      console.log('Token starts with:', this.apiToken.substring(0, 4));
      
      // Use current date and 6 months ahead for testing
      const today = new Date();
      const futureDate = new Date();
      futureDate.setMonth(today.getMonth() + 6);
      
      const startDate = this.formatDateForAPI(today);
      const endDate = this.formatDateForAPI(futureDate);
      
      console.log('Formatted dates:', { startDate, endDate });
      
      const testUrl = `${this.baseURL}/events?sort=date&start=${startDate}&end=${endDate}&orderdirection=asc`;
      console.log('Test URL:', testUrl);
      
      // Test with proper headers for localhost/container requests
      const headers = {
        'token': this.apiToken,
        'accept': 'application/json',
        'User-Agent': 'Club77-CheckinApp/1.0 (https://checkin.projekt-ai.net)',
        'Origin': 'https://checkin.projekt-ai.net',
        'Referer': 'https://checkin.projekt-ai.net/',
        'Host': 'muzeek.com',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
      };
      
      console.log('Request headers:', headers);
      
      const response = await axios.get(testUrl, {
        headers: headers,
        timeout: 30000,
        validateStatus: function (status) {
          return status < 500; // Accept any status less than 500 as success for debugging
        }
      });
      
      console.log('API test response status:', response.status);
      console.log('Response headers:', response.headers);
      console.log('Response data type:', typeof response.data);
      console.log('Response data length:', Array.isArray(response.data) ? response.data.length : 'Not an array');
      
      if (response.status === 200) {
      return {
        success: true,
        message: 'Muzeek API connection successful',
          status: response.status,
          eventCount: Array.isArray(response.data) ? response.data.length : 0
        };
      } else {
        console.log('Non-200 response data:', response.data);
        return {
          success: false,
          message: 'Muzeek API returned non-200 status',
          status: response.status,
          error: response.data
      };
      }
    } catch (error) {
      console.log('=== MUZEEK API ERROR DEBUG ===');
      console.error('Error testing Muzeek connection:', error.response?.data || error.message);
      console.error('Error status:', error.response?.status);
      console.error('Error headers:', error.response?.headers);
      console.error('Request config:', error.config);
      console.error('Full error:', error);
      return {
        success: false,
        message: 'Muzeek API connection failed',
        error: error.response?.data || error.message,
        status: error.response?.status
      };
    }
  }

  // Get events from Muzeek API with proper filtering
  async getEvents() {
    try {
      console.log('Fetching events from Muzeek API...');
      console.log('API Token:', this.apiToken.substring(0, 10) + '...');
      console.log('Base URL:', this.baseURL);
      
      // Get events for the next year, starting from today
      const today = new Date();
      const futureDate = new Date();
      futureDate.setFullYear(today.getFullYear() + 1);
      
      // Format dates correctly for Muzeek API (DD-MM-YYYY)
      const startDate = this.formatDateForAPI(today);
      const endDate = this.formatDateForAPI(futureDate);
      
      console.log('Date range:', startDate, 'to', endDate);
      
      // Build query parameters exactly as shown in API documentation
      const params = {
        sort: 'date',
        start: startDate,
        end: endDate,
        orderdirection: 'asc'
      };
      
      console.log('Query parameters:', params);
      
      // Make the API call using the client with proper headers
      const response = await this.client.get('/events', { params });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers['content-type']);
      
      const eventsData = response.data;
      
      // Ensure we have an array
      if (!Array.isArray(eventsData)) {
        console.error('API did not return an array:', typeof eventsData);
        return {
          success: false,
          error: 'API returned invalid data format',
          events: []
        };
      }
      
      console.log(`Found ${eventsData.length} total events from Muzeek API`);
      
      // Filter for announced events only (as per API response, status should be "announced")
      const announcedEvents = eventsData.filter(event => {
        const status = event.status?.toLowerCase();
        const isAnnounced = status === 'announced';
        
        // Log first few events for debugging
        if (eventsData.indexOf(event) < 3) {
          console.log(`Event ${event.id}: ${event.title}`);
          console.log(`  Status: ${status}`);
          console.log(`  Date: ${event.date}`);
          console.log(`  Location: ${event.location}`);
          console.log(`  Is announced: ${isAnnounced}`);
        }
        
        return isAnnounced;
      });
      
      console.log(`Filtered to ${announcedEvents.length} announced events`);
      
      return {
        success: true,
        events: announcedEvents,
        total: eventsData.length,
        live: announcedEvents.length
      };
      
    } catch (error) {
      console.error('Error fetching Muzeek events:', error.response?.data || error.message);
      console.error('Error status:', error.response?.status);
      console.error('Request config:', error.config);
      return {
        success: false,
        error: error.response?.data || error.message,
        events: []
      };
    }
  }

  // Convert time string to MySQL TIME format (HH:MM:SS)
  convertTimeToMySQLFormat(timeString) {
    if (!timeString) return null;
    
    // Handle various time formats
    const timeStr = timeString.toString().toLowerCase().trim();
    
    // If already in HH:MM:SS format, return as is
    if (/^\d{2}:\d{2}:\d{2}$/.test(timeStr)) {
      return timeStr;
    }
    
    // Parse 12-hour format (e.g., "10:00 PM", "10:00pm", "10pm")
    const match = timeStr.match(/(\d{1,2})(?::(\d{2}))?\s*(am|pm)/);
    if (match) {
      let hours = parseInt(match[1]);
      const minutes = match[2] ? parseInt(match[2]) : 0;
      const period = match[3];
      
      // Convert to 24-hour format
      if (period === 'pm' && hours !== 12) {
        hours += 12;
      } else if (period === 'am' && hours === 12) {
        hours = 0;
      }
      
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:00`;
    }
    
    // If no match, return null
    return null;
  }

  // Transform Muzeek event data to our database format
  transformEventData(muzeekEvent) {
    return {
      muzeek_id: muzeekEvent.id,
      name: muzeekEvent.title || muzeekEvent.name,
      description: muzeekEvent.description || muzeekEvent.description_html,
      event_date: muzeekEvent.date,
      start_time: this.convertTimeToMySQLFormat(muzeekEvent.start_time || '10:00 PM'),
      end_time: this.convertTimeToMySQLFormat(muzeekEvent.end_time || '5:00 AM'),
      venue: muzeekEvent.location || 'Club 77',
      artwork_url: muzeekEvent.flyer_image || muzeekEvent.flyer_url,
      is_live: muzeekEvent.status?.toLowerCase() === 'announced',
      muzeek_published: true,
      last_synced: new Date()
    };
  }

  // Sync events from Muzeek to local database
  async syncEvents() {
    try {
      console.log('Starting Muzeek events sync...');
      
      const result = await this.getEvents();
      
      if (!result.success) {
        return result;
      }
      
      // Transform events to our format
      const transformedEvents = result.events.map(event => this.transformEventData(event));
      
      console.log(`Transformed ${transformedEvents.length} events for database sync`);
      
      return {
        success: true,
        events: transformedEvents,
        total: result.total,
        live: result.live
      };
      
    } catch (error) {
      console.error('Error syncing Muzeek events:', error.message);
      return {
        success: false,
        error: error.message,
        events: []
      };
    }
  }

  // Get specific event by ID
  async getEvent(eventId) {
    try {
      const response = await this.client.get(`/events/${eventId}`);
      return {
        success: true,
        event: this.transformEventData(response.data)
      };
    } catch (error) {
      console.error('Error fetching Muzeek event:', error.response?.data || error.message);
      return {
        success: false,
        error: error.response?.data || error.message
      };
    }
  }
}

module.exports = MuzeekService; 