-- Create the database
CREATE DATABASE IF NOT EXISTS club77;
USE club77;

-- Create events table
CREATE TABLE IF NOT EXISTS events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  event_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create guests table
CREATE TABLE IF NOT EXISTS guests (
  id INT AUTO_INCREMENT PRIMARY KEY,
  event_id INT NOT NULL,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  dob DATE,
  checked_in BOOLEAN DEFAULT FALSE,
  check_in_time TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- Create users table for admin access
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  is_admin BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default admin user (username: admin, password: club77admin)
INSERT INTO users (username, password, is_admin) 
VALUES ('admin', '$2a$10$X7BfIFH/g.x5Ie9M5C7SiOZHUDu7JE8Yd6Z7zq3rKE5TUz5WmWNnm', TRUE);

-- Insert sample events
INSERT INTO events (name, event_date) VALUES
('Friday Night Live', '2025-06-01'),
('Saturday Night Party', '2025-06-02'),
('Sunday Sessions', '2025-06-03');

-- Insert sample guests
INSERT INTO guests (event_id, first_name, last_name, email, dob, checked_in) VALUES
(1, 'John', 'Doe', 'john@example.com', '1990-01-15', FALSE),
(1, 'Jane', 'Smith', 'jane@example.com', '1992-05-20', FALSE),
(1, 'Michael', 'Johnson', 'michael@example.com', '1988-11-03', FALSE),
(2, 'Sarah', 'Williams', 'sarah@example.com', '1995-07-12', FALSE),
(2, 'Robert', 'Brown', 'robert@example.com', '1987-09-28', FALSE),
(3, 'Emily', 'Davis', 'emily@example.com', '1993-03-17', FALSE),
(3, 'James', 'Miller', 'james@example.com', '1991-12-05', FALSE);

-- Create index for faster queries
CREATE INDEX idx_event_id ON guests(event_id);
CREATE INDEX idx_name ON guests(first_name, last_name);
CREATE INDEX idx_checked_in ON guests(checked_in); 