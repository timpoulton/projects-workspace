USE club77;

-- Add muzeek_id column if it doesn't exist
ALTER TABLE events ADD COLUMN muzeek_id VARCHAR(255) NULL UNIQUE;

-- Add muzeek_published column if it doesn't exist  
ALTER TABLE events ADD COLUMN muzeek_published BOOLEAN DEFAULT FALSE;

-- Show final table structure
DESCRIBE events; 