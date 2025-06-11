require('dotenv').config();
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const flash = require('connect-flash');
const morgan = require('morgan');
const ejsLayouts = require('express-ejs-layouts');
const { Sequelize } = require('sequelize');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3001;

// Database connection
const sequelize = new Sequelize(
  process.env.DB_NAME || 'club77', 
  process.env.DB_USER || 'root', 
  process.env.DB_PASSWORD || 'password', 
  {
    host: process.env.DB_HOST || 'localhost',
    dialect: 'mysql',
    logging: false
  }
);

// Test database connection
async function testDbConnection() {
  try {
    await sequelize.authenticate();
    console.log('Database connection established successfully.');
  } catch (error) {
    console.error('Unable to connect to the database:', error);
  }
}
testDbConnection();

// Import models
const models = require('./models');

// Middleware
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// Session configuration
app.use(session({
  secret: process.env.SESSION_SECRET || 'club77secret',
  resave: false,
  saveUninitialized: true,
  cookie: { maxAge: 3600000 } // 1 hour
}));

// Flash messages
app.use(flash());

// Global variables
app.use((req, res, next) => {
  res.locals.success_msg = req.flash('success_msg');
  res.locals.error_msg = req.flash('error_msg');
  res.locals.error = req.flash('error');
  next();
});

// View engine setup
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Conditional layout middleware - skip layout for main pages
app.use((req, res, next) => {
  // Skip layout for main pages that have their own complete HTML
  if (req.path === '/' || req.path.startsWith('/events/')) {
    res.locals.layout = false;
  } else {
    // Use layout for other pages (login, search, etc.)
    res.locals.layout = 'layout';
  }
  next();
});

// app.use(ejsLayouts); // Temporarily disabled for Tailwind redesign
// app.set('layout', 'layout'); // Temporarily disabled for Tailwind redesign

// Routes
const indexRouter = require('./routes/index');
const eventRouter = require('./routes/events');
const guestRouter = require('./routes/guests');
const webhookRouter = require('./routes/webhooks');
const syncRouter = require('./routes/sync');

app.use('/', indexRouter);
app.use('/events', eventRouter);
app.use('/guests', guestRouter);
app.use('/api/webhooks', webhookRouter);
app.use('/api/sync', syncRouter);

// Error handling
app.use((req, res, next) => {
  res.status(404).render('error', { 
    title: 'Page Not Found',
    message: 'The page you requested could not be found.',
    error: { status: 404 }
  });
});

app.use((err, req, res, next) => {
  res.status(err.status || 500).render('error', {
    title: 'Error',
    message: err.message,
    error: process.env.NODE_ENV === 'development' ? err : {}
  });
});

// Auto-sync Muzeek events on startup
async function autoSyncOnStartup() {
  try {
    const MuzeekService = require('./services/muzeek');
    const { Event } = require('./models');
    
    // Check if we have any events
    const eventCount = await Event.count();
    
    if (eventCount === 0) {
      console.log('No events found, triggering initial Muzeek sync...');
      const muzeekService = new MuzeekService();
      const syncResult = await muzeekService.syncEvents();
      
      if (syncResult.success) {
        // Save events to database
        for (const eventData of syncResult.events) {
          try {
            // Check if event already exists
            const existingEvent = await Event.findOne({
              where: { muzeek_id: eventData.muzeek_id }
            });
            
            if (!existingEvent) {
              // Only create if it doesn't exist
              await Event.create(eventData);
            }
          } catch (error) {
            console.error(`Error saving event ${eventData.name}:`, error.message);
          }
        }
        console.log(`Startup sync completed: ${syncResult.events.length} events synced`);
      } else {
        console.error('Startup sync failed:', syncResult.error);
      }
    } else {
      console.log(`Found ${eventCount} existing events, skipping startup sync`);
    }
  } catch (error) {
    console.error('Error during startup sync:', error.message);
  }
}

// Start server
sequelize.sync().then(async () => {
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
  
  // Run auto-sync after server starts
  setTimeout(autoSyncOnStartup, 2000); // Wait 2 seconds for server to be ready
}).catch(err => {
  console.error('Failed to sync database:', err);
});

module.exports = app; 