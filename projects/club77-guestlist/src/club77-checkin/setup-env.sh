#!/bin/bash

# Create .env file
cat > .env << EOL
# Database Configuration
DB_NAME=club77
DB_USER=root
DB_PASSWORD=lkj654
DB_HOST=localhost

# App Configuration
PORT=3001
SESSION_SECRET=club77_session_secret_key

# Mailchimp Configuration
MAILCHIMP_API_KEY=your-mailchimp-api-key
MAILCHIMP_SERVER=us10
MAILCHIMP_LIST_ID=53f56e2c77

# Webflow Webhook Secret
WEBFLOW_WEBHOOK_SECRET=9beb0bcdcc51ef40cffc539947b47055898885e96931d0bb0a5009ab4696e6a6
EOL

echo ".env file created successfully" 