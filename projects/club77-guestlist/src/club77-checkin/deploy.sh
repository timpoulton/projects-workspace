#!/bin/bash

# Club77 Guest Check-In System Deployment Script
# This script automates the deployment of the Club77 Check-In System

# Exit on any error
set -e

echo "=== Club77 Guest Check-In System Deployment ==="
echo "This script will install and configure the application."

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Error: Please run this script as root or with sudo."
    exit 1
fi

# Check dependencies
echo "Checking dependencies..."
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm is required but not installed. Aborting."; exit 1; }
command -v mysql >/dev/null 2>&1 || { echo "MySQL is required but not installed. Aborting."; exit 1; }

# Current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Setup database
echo "Setting up database..."
read -p "MySQL root password: " MYSQL_ROOT_PASSWORD

# Create database and user
echo "Creating database and user..."
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF
CREATE DATABASE IF NOT EXISTS club77;
CREATE USER IF NOT EXISTS 'club77user'@'localhost' IDENTIFIED BY 'club77pass';
GRANT ALL PRIVILEGES ON club77.* TO 'club77user'@'localhost';
FLUSH PRIVILEGES;
EOF

# Import initial data
echo "Importing initial data..."
mysql -u club77user -p'club77pass' club77 < init-db.sql

# Setup systemd service
echo "Setting up systemd service..."
cp club77-checkin.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable club77-checkin.service

# Start service
echo "Starting service..."
systemctl start club77-checkin.service

# Display status
echo "Checking service status..."
systemctl status club77-checkin.service

# Display success message
echo ""
echo "=== Deployment Complete ==="
echo "The Club77 Guest Check-In System has been deployed successfully."
echo "Access the application at: http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo "Default login credentials:"
echo "Username: admin"
echo "Password: club77admin"

exit 0 