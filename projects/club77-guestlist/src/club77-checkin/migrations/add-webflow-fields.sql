-- Add Webflow integration fields to events table
-- Run this migration to add support for Webflow API integration

ALTER TABLE events 
ADD COLUMN webflow_id VARCHAR(255) NULL UNIQUE,
ADD COLUMN webflow_slug VARCHAR(255) NULL,
ADD COLUMN description TEXT NULL,
ADD COLUMN artwork_url VARCHAR(500) NULL,
ADD COLUMN start_time VARCHAR(50) NULL DEFAULT '10:00 PM',
ADD COLUMN end_time VARCHAR(50) NULL DEFAULT '5:00 AM',
ADD COLUMN venue VARCHAR(255) NULL DEFAULT '77 William St, Darlinghurst',
ADD COLUMN is_live BOOLEAN NOT NULL DEFAULT TRUE,
ADD COLUMN webflow_published BOOLEAN NOT NULL DEFAULT FALSE,
ADD COLUMN last_synced DATETIME NULL;

-- Create index on webflow_id for faster lookups
CREATE INDEX idx_events_webflow_id ON events(webflow_id);

-- Create index on is_live for filtering
CREATE INDEX idx_events_is_live ON events(is_live);

-- Update existing events to be live by default
UPDATE events SET is_live = TRUE WHERE is_live IS NULL; 