#!/usr/bin/env bash
set -e
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME=$(basename "$BASE_DIR")
MEMORY_FILE="$BASE_DIR/$PROJECT_NAME Memory.md"
if [ ! -f "$MEMORY_FILE" ]; then
  echo "Memory file not found: $MEMORY_FILE"
  exit 1
fi
echo "Starting chat with AI using project memory: $MEMORY_FILE"
# Construct system prompt with memory contents
SYSTEM_PROMPT="system: |\n$(sed 's/^/  /' "$MEMORY_FILE")"

# Parse flags
UPDATE_MEMORY=false
RESUME=false
WORKFLOW=false
PROMPTS=()
for arg in "$@"; do
  case "$arg" in
    --update-memory) UPDATE_MEMORY=true ;; 
    --resume) RESUME=true ;; 
    --workflow) WORKFLOW=true ;; 
    *) PROMPTS+=("$arg") ;; 
  esac
done

# If workflow flag, display the chat workflow and exit
if [ "$WORKFLOW" = true ]; then
  cat "$BASE_DIR/CHAT_WORKFLOW.md"
  exit 0
fi

# Handle interactive or single-prompt mode
if [ ${#PROMPTS[@]} -gt 0 ]; then
  for p in "${PROMPTS[@]}"; do
    call_ai "$p"
  done
else
  echo "Enter your prompt (Ctrl+D to end):"
  while IFS= read -r line; do
    # Detect manual workflow trigger phrase
    if [[ "${line,,}" == "enter workflow mode" ]]; then
      cat "$BASE_DIR/CHAT_WORKFLOW.md"
      continue
    fi
    call_ai "$line"
  done
fi
