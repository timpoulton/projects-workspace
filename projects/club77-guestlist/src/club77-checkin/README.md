# Club77 Check-In System

## 🏷️ Service Classification

**Category:** C (Business) | **Port:** 3001 | **Status:** ✅ Active  
**Domain:** checkin.projekt-ai.net | **SSL:** ✅ Required | **Deployment:** Docker ✅

---

## 📋 Overview

Professional Apple-inspired web application for managing guest check-ins at Club77 events. Features real-time Webflow integration, mobile-first design optimized for staff operations, and seamless event management.

### 🎯 Key Features

- ✅ **Webflow Integration** - Automatic sync with Club77 website events
- ✅ **Apple Design System** - Professional iOS-inspired interface  
- ✅ **Mobile-First** - Touch-optimized for staff devices
- ✅ **Real-Time Updates** - Live guest list management
- ✅ **Event Artwork** - Official event posters from Webflow
- ✅ **Multi-Event Support** - Handle multiple simultaneous events
- ✅ **Haptic Feedback** - Enhanced mobile experience

## 🏗️ Architecture

### Technology Stack
- **Backend:** Node.js 18+ with Express.js
- **Database:** MySQL 8.0 (containerized)
- **Frontend:** EJS templates with Apple Design System
- **API Integration:** Webflow Data API v2.0.0
- **Authentication:** Express sessions (secure)
- **Deployment:** Docker Compose (standardized)

### Container Structure
```
club77-checkin/
├── club77_app     (Node.js application)
├── club77_db      (MySQL 8.0 database)
└── club77_network (Docker network)
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Access to 192.168.1.107 (homelab server)
- Webflow API token (configured)

### Deployment (Standardized)
```bash
# Navigate to standardized location
cd /srv/apps/club77-checkin

# Start services
docker-compose up -d

# Verify deployment
docker ps | grep club77
curl -s -o /dev/null -w "%{http_code}" http://localhost:3001
```

### Access Points
- **Internal:** http://192.168.1.107:3001
- **External:** https://checkin.projekt-ai.net
- **Development:** http://localhost:3001

## 🔧 Configuration

### Environment Variables
```env
# Application
PORT=3001
NODE_ENV=production

# Database (containerized)
DB_HOST=db
DB_USER=root
DB_PASSWORD=lkj654
DB_NAME=club77

# Security
SESSION_SECRET=club77secret_secure_key_2024

# Webflow Integration
WEBFLOW_API_TOKEN=f0840501141e3949ac2c4bfe2dd0c8f4b5acfd8e5ae3bfd7e428b3b12b360651
WEBFLOW_SITE_ID=659df657bfc102e175b74a93

# Webhooks
WEBFLOW_WEBHOOK_SECRET=9beb0bcdcc51ef40cffc539947b47055898885e96931d0bb0a5009ab4696e6a6
```

### Database Schema
```sql
-- Enhanced Events Table (with Webflow integration)
CREATE TABLE events (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  date DATE NOT NULL,
  webflow_id VARCHAR(255) UNIQUE,
  webflow_slug VARCHAR(255),
  description TEXT,
  artwork_url VARCHAR(500),
  start_time DATETIME,
  end_time DATETIME,
  venue VARCHAR(255),
  is_live BOOLEAN DEFAULT false,
  webflow_published BOOLEAN DEFAULT false,
  last_synced TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Guests Table
CREATE TABLE guests (
  id INT PRIMARY KEY AUTO_INCREMENT,
  event_id INT NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(20),
  checked_in BOOLEAN DEFAULT false,
  check_in_time TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
```

## 🎨 Apple Design System

### Design Principles
- **Typography Excellence:** SF Pro font family
- **Color Mastery:** Apple system colors
- **Motion & Animation:** Cubic-bezier easing
- **Glassmorphism:** Backdrop blur effects
- **Touch Optimization:** 44pt minimum targets

### CSS Variables
```css
:root {
  --system-background: #ffffff;
  --system-foreground: #000000;
  --system-blue: #007AFF;
  --system-gray: #8E8E93;
  --system-gray-2: #AEAEB2;
  --system-gray-3: #C7C7CC;
  --system-gray-4: #D1D1D6;
  --system-gray-5: #E5E5EA;
  --system-gray-6: #F2F2F7;
}
```

## 🔗 Webflow Integration

### API Configuration
- **Version:** Webflow Data API v2.0.0
- **Site ID:** 659df657bfc102e175b74a93
- **Collection:** Events (Club77 website)
- **Sync:** Manual + automatic detection

### Sync Features
- ✅ Pull live events from website
- ✅ Display official event artwork
- ✅ Filter published/live events only
- ✅ Link events to guest lists
- ✅ Error handling & fallbacks

### API Endpoints
```javascript
POST /api/sync/webflow/events    // Manual sync trigger
GET  /api/sync/webflow/status    // Sync status check
GET  /api/sync/webflow/test      // Connection test
```

## 📱 Mobile Optimization

### Touch Features
- **Haptic Feedback** - Vibration on interactions
- **Touch Targets** - 44pt minimum size
- **Gesture Support** - Swipe and tap optimized
- **Responsive Design** - Mobile-first approach
- **Performance** - Hardware acceleration

### iOS-Style Components
- **Segmented Control** - UPCOMING/PAST toggle
- **Cards** - Event and guest cards
- **Buttons** - Pill-shaped with animations
- **Navigation** - iOS-style transitions

## 🔒 Security

### Authentication
```javascript
// Default Credentials (Change in production)
Username: admin
Password: club77admin

// Session Configuration
{
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,      // HTTPS only
    httpOnly: true,    // XSS protection
    maxAge: 3600000    // 1 hour
  }
}
```

### Security Features
- ✅ HTTPS enforced
- ✅ Secure session cookies
- ✅ SQL injection prevention
- ✅ CORS protection
- ✅ Rate limiting

## 📊 API Reference

### Core Endpoints
```javascript
// Event Management
GET    /api/events              // List all events
GET    /api/events/:id          // Get specific event
POST   /api/events              // Create new event
PUT    /api/events/:id          // Update event
DELETE /api/events/:id          // Delete event

// Guest Management
GET    /api/guests              // List all guests
GET    /api/guests/event/:id    // Guests for specific event
POST   /api/guests              // Add new guest
PUT    /api/guests/:id/checkin  // Check in guest
PUT    /api/guests/:id/checkout // Check out guest

// System Health
GET    /health                  // Application health
GET    /api/health/db          // Database health
```

## 🎯 Usage Guide

### For Club77 Staff
1. **Access:** Visit https://checkin.projekt-ai.net
2. **Login:** Use provided credentials
3. **Sync Events:** Click "Sync Events" for latest from website
4. **Select Event:** Choose event card to manage
5. **Check-in Guests:** Use mobile interface for arrivals
6. **Search:** Real-time guest search
7. **Statistics:** View live attendance metrics

### For Event Management
1. **Webflow CMS:** Add/edit events on website
2. **Set Live Status:** Ensure events are published
3. **Include Artwork:** Add event posters in Webflow
4. **Auto-Sync:** System detects and syncs new events

## 🔧 Maintenance

### Health Checks
```bash
# Application health
curl https://checkin.projekt-ai.net/health

# Container status
docker ps | grep club77

# Database connectivity
docker exec club77_db mysql -u root -plkj654 -e "SELECT 1"
```

### Backup Procedures
```bash
# Database backup
docker exec club77_db mysqldump -u root -plkj654 club77 > backup_$(date +%Y%m%d_%H%M%S).sql

# Application backup
tar -czf club77-backup-$(date +%Y%m%d).tar.gz /srv/apps/club77-checkin
```

### Updates
```bash
# Update deployment
cd /srv/apps/club77-checkin
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verify update
curl -s -o /dev/null -w "%{http_code}" https://checkin.projekt-ai.net
```

## 🚨 Troubleshooting

### Common Issues

**Container won't start:**
```bash
docker-compose logs app
cat .env
docker-compose restart
```

**Database connection errors:**
```bash
docker ps | grep club77_db
docker exec club77_db mysql -u root -plkj654 -e "SELECT 1"
```

**Webflow sync issues:**
```bash
curl -H "Authorization: Bearer $WEBFLOW_API_TOKEN" \
     "https://api.webflow.com/v2/sites/659df657bfc102e175b74a93"
```

## 📋 Standardization Compliance

### Homelab Framework Adherence
- ✅ **Category C Classification** - Business service
- ✅ **Port 3001** - Standardized assignment
- ✅ **Docker Deployment** - Containerized
- ✅ **nginx Reverse Proxy** - External access
- ✅ **SSL Certificate** - Let's Encrypt
- ✅ **Documentation** - Comprehensive
- ✅ **Monitoring** - Health checks
- ✅ **Backup Procedures** - Automated

### PORT-TRACKER.md Entry
```
3001 | Club77 Check-In | Category C | Docker | checkin.projekt-ai.net | ✅ Active
```

## 📞 Support

**Status:** ✅ Fully Operational  
**Last Updated:** 2025-05-25  
**Documentation:** [Full Documentation](../../documentation/apps/club77-checkin.md)

**Emergency Contacts:**
- System Administrator: root@192.168.1.107
- Application Logs: `docker logs club77_app`
- Monitoring: Docker health checks

---

*This application follows the homelab standardization framework for consistent, maintainable infrastructure.* 