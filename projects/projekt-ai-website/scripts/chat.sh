#!/usr/bin/env bash
set -e

# Determine project root and name
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME=$(basename "$BASE_DIR")

# Load environment variables from deploy/.env if present
if [ -f "$BASE_DIR/deploy/.env" ]; then
  set -o allexport
  source "$BASE_DIR/deploy/.env"
  set +o allexport
fi

# Ensure logs directory exists
mkdir -p "$BASE_DIR/logs"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
LOG_FILE="$BASE_DIR/logs/chat-$TIMESTAMP.log"

# Parse flags
UPDATE_MEMORY=false
RESUME=false
WORKFLOW=false
PROMPTS=()
for arg in "$@"; do
  case "$arg" in
    --update-memory) UPDATE_MEMORY=true ;;  
    --resume)       RESUME=true       ;;  
    --workflow)     WORKFLOW=true     ;;  
    *)              PROMPTS+=("$arg") ;;  
  esac
done

# If workflow flag, display the chat workflow and exit
if [ "$WORKFLOW" = true ]; then
  cat "$BASE_DIR/CHAT_WORKFLOW.md"
  exit 0
fi

# Locate project memory file
MEMORY_FILE=$(find "$BASE_DIR" -maxdepth 1 -type f -name "*Memory.md" | head -n1)
if [ -z "$MEMORY_FILE" ]; then
  echo "Memory file not found in $BASE_DIR"
  exit 1
fi

# If update-memory flag, summarize last chat and append to memory
if [ "$UPDATE_MEMORY" = true ]; then
  LAST_LOG=$(ls -1t "$BASE_DIR/logs/chat-*.log" | head -n1)
  SUMMARY=$(openai api chat.completions.create \
    -m gpt-4-turbo \
    -p "Summarize the following chat in Markdown bullets under headings 'Technical Decisions' and 'Preferences':

$(sed 's/"/\"/g' "$LAST_LOG")")
  echo -e "
$SUMMARY" >> "$MEMORY_FILE"
  echo "Memory file updated."
  exit 0
fi

# Load history if resume flag is set
HISTORY=""
if [ "$RESUME" = true ]; then
  LAST_LOG=$(ls -1t "$BASE_DIR/logs/chat-*.log" | head -n1)
  HISTORY=$(sed 's/^/  /' "$LAST_LOG")
fi

# Function to call AI and log the conversation
call_ai() {
  local input="$1"
  echo "User: $input" >> "$LOG_FILE"
  local SYS="system: |\n  $(sed 's/^/  /' "$MEMORY_FILE")"
  [ -n "$HISTORY" ] && SYS+="\nconversation: |\n$HISTORY"
  RESPONSE=$(openai api chat.completions.create -m gpt-4-turbo -p "$SYS\n\nuser: $input")
  echo -e "\nAssistant: $RESPONSE\n" >> "$LOG_FILE"
  echo "$RESPONSE"
}

# Handle interactive or single-prompt mode
if [ ${#PROMPTS[@]} -gt 0 ]; then
  for p in "${PROMPTS[@]}"; do
    call_ai "$p"
  done
else
  echo "Enter your prompt (Ctrl+D to end, 'enter workflow mode' to view instructions):"
  while IFS= read -r line; do
    if [[ "${line,,}" == "enter workflow mode" ]]; then
      cat "$BASE_DIR/CHAT_WORKFLOW.md"
      continue
    fi
    call_ai "$line"
  done
fi
