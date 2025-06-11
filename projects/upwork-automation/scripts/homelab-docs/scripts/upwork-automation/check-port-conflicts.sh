#!/bin/bash

# Check Port Conflicts Script
# Used to identify and resolve port conflicts in the Upwork automation system
# Created: June 3, 2025

# Standard logging format
log_info() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1"
}

log_error() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1" >&2
}

log_success() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [SUCCESS] $1"
}

# Configuration
PROPOSAL_SERVER_PORT=5001
API_SERVER_PORT=5050
LOG_FILE="port-conflicts-$(date +%Y%m%d-%H%M%S).log"
SCRIPTS_DIR="/root/homelab-docs/scripts/upwork-automation"

# Create log file
touch "${SCRIPTS_DIR}/${LOG_FILE}"
log_info "Starting port conflict check" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"

# Check if a port is in use
check_port() {
  local port=$1
  local service_name=$2
  
  log_info "Checking port ${port} for service ${service_name}..." | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
  
  # Use lsof to check if port is in use
  local process_info=$(lsof -i :${port} -P -n 2>/dev/null)
  
  if [ -n "$process_info" ]; then
    # Port is in use
    local pid=$(echo "$process_info" | grep -v "PID" | awk '{print $2}' | head -n 1)
    local process_name=$(ps -p $pid -o comm= 2>/dev/null)
    local command=$(ps -p $pid -o cmd= 2>/dev/null)
    
    log_info "Port ${port} is in use by PID ${pid} (${process_name})" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
    log_info "Command: ${command}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
    
    return 0  # Port is in use
  else
    log_success "Port ${port} is available" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
    return 1  # Port is available
  fi
}

# Kill process on port safely
kill_process_on_port() {
  local port=$1
  local force=$2
  
  log_info "Attempting to kill process on port ${port}..." | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
  
  # Find process on port
  local pid=$(lsof -i :${port} -t 2>/dev/null)
  
  if [ -n "$pid" ]; then
    # Get process info before killing
    local process_name=$(ps -p $pid -o comm= 2>/dev/null)
    
    if [ "$force" = "force" ]; then
      log_info "Force killing process ${pid} (${process_name}) on port ${port}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      kill -9 $pid 2>/dev/null
    else
      log_info "Gracefully stopping process ${pid} (${process_name}) on port ${port}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      kill $pid 2>/dev/null
      
      # Wait up to 5 seconds for process to exit
      for i in {1..5}; do
        if ! lsof -i :${port} -t &>/dev/null; then
          break
        fi
        sleep 1
      done
      
      # Force kill if still running
      if lsof -i :${port} -t &>/dev/null; then
        log_info "Process still running, force killing..." | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
        kill -9 $pid 2>/dev/null
      fi
    fi
    
    # Verify port is now available
    if ! lsof -i :${port} -t &>/dev/null; then
      log_success "Successfully killed process on port ${port}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      return 0
    else
      log_error "Failed to kill process on port ${port}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      return 1
    fi
  else
    log_info "No process found on port ${port}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
    return 0
  fi
}

# Check for zombie Python processes
check_zombie_processes() {
  log_info "Checking for zombie Python processes..." | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
  
  # Find Python processes
  local python_processes=$(ps aux | grep python | grep -v grep)
  
  if [ -n "$python_processes" ]; then
    log_info "Found Python processes:" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
    echo "$python_processes" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
    
    # Check for zombie state processes
    local zombie_processes=$(ps aux | grep python | grep defunct | grep -v grep)
    
    if [ -n "$zombie_processes" ]; then
      log_error "Found zombie Python processes:" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      echo "$zombie_processes" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      
      # Try to clean up zombie processes
      log_info "Attempting to clean up zombie processes..." | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      
      echo "$zombie_processes" | awk '{print $2}' | xargs -r kill -9 2>/dev/null
      
      # Check if zombies are gone
      if ! ps aux | grep python | grep defunct | grep -v grep &>/dev/null; then
        log_success "Successfully cleaned up zombie processes" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      else
        log_error "Failed to clean up all zombie processes" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      fi
    else
      log_success "No zombie Python processes found" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
    fi
  else
    log_info "No Python processes found" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
  fi
}

# List all active services related to our system
list_related_services() {
  log_info "Listing all related services..." | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
  
  # Check for systemd services
  local services=$(systemctl list-units --type=service | grep -E 'upwork|proposal' | tee -a "${SCRIPTS_DIR}/${LOG_FILE}")
  
  if [ -n "$services" ]; then
    log_info "Found related systemd services:" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
    echo "$services" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
  else
    log_info "No related systemd services found" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
  fi
  
  # Check all listening ports
  log_info "Listing all listening ports:" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
  netstat -tuln | grep LISTEN | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
}

# Main execution starts here
log_info "===== Port Conflict Detection and Resolution =====" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"

# First, check zombie processes
check_zombie_processes

# List all related services
list_related_services

# Check proposal server port
if check_port $PROPOSAL_SERVER_PORT "Proposal Server"; then
  echo ""
  echo "Port ${PROPOSAL_SERVER_PORT} is in use. What would you like to do?"
  echo "1) Kill process gracefully"
  echo "2) Force kill process"
  echo "3) Change port in configuration"
  echo "4) Do nothing"
  read -p "Select an option (1-4): " option
  
  case $option in
    1)
      kill_process_on_port $PROPOSAL_SERVER_PORT
      ;;
    2)
      kill_process_on_port $PROPOSAL_SERVER_PORT "force"
      ;;
    3)
      log_info "Manual port configuration change selected" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      echo "Please edit the PORT variable in upwork-proposal-server.py and other related files."
      ;;
    *)
      log_info "No action taken for port ${PROPOSAL_SERVER_PORT}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      ;;
  esac
fi

# Check API server port
if check_port $API_SERVER_PORT "API Server"; then
  echo ""
  echo "Port ${API_SERVER_PORT} is in use. What would you like to do?"
  echo "1) Kill process gracefully"
  echo "2) Force kill process"
  echo "3) Change port in configuration"
  echo "4) Do nothing"
  read -p "Select an option (1-4): " option
  
  case $option in
    1)
      kill_process_on_port $API_SERVER_PORT
      ;;
    2)
      kill_process_on_port $API_SERVER_PORT "force"
      ;;
    3)
      log_info "Manual port configuration change selected" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      echo "Please edit the PORT variable in api-server.py and update the Nginx configuration."
      ;;
    *)
      log_info "No action taken for port ${API_SERVER_PORT}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
      ;;
  esac
fi

# Final status report
echo ""
log_info "===== Final Port Status =====" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
log_info "Proposal Server Port (${PROPOSAL_SERVER_PORT}): $(lsof -i :${PROPOSAL_SERVER_PORT} -P -n 2>/dev/null || echo 'Available')" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"
log_info "API Server Port (${API_SERVER_PORT}): $(lsof -i :${API_SERVER_PORT} -P -n 2>/dev/null || echo 'Available')" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"

log_success "Port conflict check completed. Log saved to ${SCRIPTS_DIR}/${LOG_FILE}" | tee -a "${SCRIPTS_DIR}/${LOG_FILE}"

# Provide recommendations
echo ""
echo "===== RECOMMENDATIONS ====="
if ! lsof -i :${PROPOSAL_SERVER_PORT} -P -n &>/dev/null && ! lsof -i :${API_SERVER_PORT} -P -n &>/dev/null; then
  echo "✅ All ports are available. You can start services now."
  echo "   To start proposal server: cd ${SCRIPTS_DIR} && python3 upwork-proposal-server.py"
  echo "   To start API server: systemctl start upwork-proposal-api"
else
  echo "⚠️  Some ports are still in use. Please resolve conflicts before starting services."
  echo "   Run this script again or manually handle the processes using the ports."
fi 