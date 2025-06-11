#!/bin/bash

echo "Rolling back test API changes..."

# Stop and disable the test service
systemctl stop upwork-proposal-api-test
systemctl disable upwork-proposal-api-test

# Remove test files
rm -f /root/homelab-docs/scripts/upwork-automation/api-server-test.py
rm -f /etc/systemd/system/upwork-proposal-api-test.service
rm -f /var/www/projekt-ai.net/api-test-safe.html
rm -f /var/www/projekt-ai.net/upwork-dashboard-test.html

# Reload systemd
systemctl daemon-reload

echo "Rollback complete. Test API removed."
