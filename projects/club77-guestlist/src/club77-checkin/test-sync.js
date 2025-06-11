const { Event } = require('./models');
const MuzeekService = require('./services/muzeek');

async function syncEvents() {
    try {
        const muzeekService = new MuzeekService();
        const syncResult = await muzeekService.syncEvents();
        
        if (!syncResult.success) {
            console.log(JSON.stringify({success: false, error: syncResult.error}));
            process.exit(1);
        }
        
        let created = 0, updated = 0;
        for (const eventData of syncResult.events) {
            const existingEvent = await Event.findOne({ where: { muzeek_id: eventData.muzeek_id } });
            if (existingEvent) {
                await existingEvent.update(eventData);
                updated++;
            } else {
                await Event.create(eventData);
                created++;
            }
        }
        
        console.log(JSON.stringify({success: true, stats: {total: syncResult.events.length, created, updated}}));
    } catch (error) {
        console.log(JSON.stringify({success: false, error: error.message}));
        process.exit(1);
    }
}

syncEvents(); 