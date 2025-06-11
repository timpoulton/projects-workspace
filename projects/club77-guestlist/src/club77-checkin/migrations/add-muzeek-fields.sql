-- Add Muzeek integration fields to events table
-- Run this migration to add support for Muzeek API integration

ALTER TABLE events 
ADD COLUMN muzeek_id VARCHAR(255) NULL UNIQUE,
ADD COLUMN muzeek_published BOOLEAN NOT NULL DEFAULT FALSE;

-- Create index on muzeek_id for faster lookups
CREATE INDEX idx_events_muzeek_id ON events(muzeek_id);

-- Create index on muzeek_published for filtering
CREATE INDEX idx_events_muzeek_published ON events(muzeek_published);

-- Note: Other fields like description, artwork_url, start_time, end_time, venue, is_live, last_synced
-- should already exist from the Webflow migration. If not, uncomment the lines below:

-- ALTER TABLE events 
-- ADD COLUMN description TEXT NULL,
-- ADD COLUMN artwork_url VARCHAR(500) NULL,
-- ADD COLUMN start_time VARCHAR(50) NULL DEFAULT '10:00 PM',
-- ADD COLUMN end_time VARCHAR(50) NULL DEFAULT '5:00 AM',
-- ADD COLUMN venue VARCHAR(255) NULL DEFAULT '77 William St, Darlinghurst',
-- ADD COLUMN is_live BOOLEAN NOT NULL DEFAULT TRUE,
-- ADD COLUMN last_synced DATETIME NULL; 