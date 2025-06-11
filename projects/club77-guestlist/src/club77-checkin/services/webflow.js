const axios = require('axios');

class WebflowService {
  constructor() {
    this.apiToken = process.env.WEBFLOW_API_TOKEN || 'f0840501141e3949ac2c4bfe2dd0c8f4b5acfd8e5ae3bfd7e428b3b12b360651';
    this.siteId = process.env.WEBFLOW_SITE_ID; // We'll need to get this
    this.baseURL = 'https://api.webflow.com/v2';
    
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Authorization': `Bearer ${this.apiToken}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
  }

  // Get site information to find the site ID
  async getSites() {
    try {
      const response = await this.client.get('/sites');
      return response.data;
    } catch (error) {
      console.error('Error fetching Webflow sites:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get collections for the site
  async getCollections(siteId) {
    try {
      const response = await this.client.get(`/sites/${siteId}/collections`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Webflow collections:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get events from Webflow (assuming there's an "Events" collection)
  async getEvents(siteId, collectionId) {
    try {
      const response = await this.client.get(`/collections/${collectionId}/items`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Webflow events:', error.response?.data || error.message);
      throw error;
    }
  }

  // Get a specific event by ID
  async getEvent(collectionId, itemId) {
    try {
      const response = await this.client.get(`/collections/${collectionId}/items/${itemId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Webflow event:', error.response?.data || error.message);
      throw error;
    }
  }

  // Transform Webflow event data to our format
  transformEventData(webflowEvent) {
    const fieldData = webflowEvent.fieldData;
    
    return {
      webflow_id: webflowEvent.id,
      webflow_slug: fieldData.slug,
      name: fieldData.name || fieldData.title,
      description: fieldData.description,
      event_date: fieldData['event-date'] || fieldData.date,
      start_time: fieldData['start-time'] || '10:00 PM',
      end_time: fieldData['end-time'] || '5:00 AM',
      venue: fieldData.venue || '77 William St, Darlinghurst',
      artwork_url: fieldData['artwork-image']?.url || fieldData.image?.url,
      is_live: fieldData['is-live'] !== false, // Default to true unless explicitly false
      webflow_published: webflowEvent.isArchived === false && webflowEvent.isDraft === false,
      last_synced: new Date()
    };
  }

  // Sync events from Webflow to local database
  async syncEvents() {
    try {
      console.log('Starting Webflow events sync...');
      
      // First, get sites to find Club77 site
      const sites = await this.getSites();
      console.log('Available sites:', sites.sites?.map(s => ({ id: s.id, displayName: s.displayName })));
      
      // Find Club77 site (you might need to adjust this logic)
      const club77Site = sites.sites?.find(site => 
        site.displayName?.toLowerCase().includes('club77') || 
        site.displayName?.toLowerCase().includes('club 77')
      );
      
      if (!club77Site) {
        throw new Error('Club77 site not found in Webflow');
      }
      
      console.log('Found Club77 site:', club77Site.displayName, 'ID:', club77Site.id);
      
      // Get collections for the site
      const collections = await this.getCollections(club77Site.id);
      console.log('Available collections:', collections.collections?.map(c => ({ id: c.id, displayName: c.displayName })));
      
      // Find events collection
      const eventsCollection = collections.collections?.find(collection =>
        collection.displayName?.toLowerCase().includes('event') ||
        collection.slug?.toLowerCase().includes('event')
      );
      
      if (!eventsCollection) {
        throw new Error('Events collection not found in Webflow');
      }
      
      console.log('Found events collection:', eventsCollection.displayName, 'ID:', eventsCollection.id);
      
      // Get events from the collection
      const webflowEvents = await this.getEvents(club77Site.id, eventsCollection.id);
      console.log(`Found ${webflowEvents.items?.length || 0} events in Webflow`);
      
      // Transform and return events data
      const transformedEvents = webflowEvents.items?.map(event => this.transformEventData(event)) || [];
      
      // Filter only live/published events
      const liveEvents = transformedEvents.filter(event => event.is_live && event.webflow_published);
      
      console.log(`Filtered to ${liveEvents.length} live events`);
      
      return {
        success: true,
        events: liveEvents,
        total: transformedEvents.length,
        live: liveEvents.length
      };
      
    } catch (error) {
      console.error('Error syncing Webflow events:', error.message);
      return {
        success: false,
        error: error.message,
        events: []
      };
    }
  }

  // Get event artwork URL
  async getEventArtwork(webflowId) {
    try {
      // This would fetch the specific event and return its artwork
      // Implementation depends on your Webflow structure
      return null;
    } catch (error) {
      console.error('Error fetching event artwork:', error.message);
      return null;
    }
  }
}

module.exports = WebflowService; 