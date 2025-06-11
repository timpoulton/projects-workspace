#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <project-name>"
  exit 1
fi

PROJECT_NAME=$1
BASE_DIR="projects/$PROJECT_NAME"

# Create directory structure
mkdir -p "$BASE_DIR/docs" "$BASE_DIR/scripts" "$BASE_DIR/src" "$BASE_DIR/backups" "$BASE_DIR/deploy"

# Create governance documents
cat > "$BASE_DIR/$PROJECT_NAME Master Document.md" <<EOF
# $PROJECT_NAME Master Document

## Project Overview
- Objective:
- Stakeholders:
- Deliverables:
- Timeline:
EOF

cat > "$BASE_DIR/$PROJECT_NAME Memory.md" <<EOF
# $PROJECT_NAME Memory

## Technical Decisions:
## Preferences:
EOF

cat > "$BASE_DIR/$PROJECT_NAME Rules.md" <<EOF
# $PROJECT_NAME Rules

1. All project folders must include:
   - Master Document
   - Memory File
   - Rules Document
EOF

# Create deployment directory with Docker scaffolding
mkdir -p "$BASE_DIR/deploy"
cat > "$BASE_DIR/deploy/Dockerfile" <<EOF
# Use official Python runtime as a parent image
FROM python:3.12-slim
WORKDIR /app
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./
ENTRYPOINT ["upwork-automation"]
EOF

cat > "$BASE_DIR/deploy/docker-compose.yml" <<EOF
version: "3.8"
services:
  app:
    build: .
    image: ${PROJECT_NAME}:latest
    env_file:
      - .env
    volumes:
      - ./src:/app
    entrypoint: ["upwork-automation"]
EOF

cat > "$BASE_DIR/deploy/.env.example" <<EOF
# Example environment variables
# e.g. API_KEY=
EOF

# Create fully automated chat wrapper script
cat > "$BASE_DIR/scripts/chat.sh" << 'EOF'
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

# Locate project memory file
MEMORY_FILE=$(find "$BASE_DIR" -maxdepth 1 -type f -name "*Memory.md" | head -n1)
if [ -z "$MEMORY_FILE" ]; then
  echo "Memory file not found in $BASE_DIR"
  exit 1
fi

# If update-memory flag, summarize last chat and append to memory
if [ "$UPDATE_MEMORY" = true ]; then
  LAST_LOG=$(ls -1t "$BASE_DIR/logs/chat-*.log" | head -n1)
  SUMMARY=$(openai api chat.completions.create -m gpt-4-turbo -p "Summarize the following chat in Markdown bullets under headings 'Technical Decisions' and 'Preferences':\n\n$(sed 's/"/\\"/g' "$LAST_LOG")")
  echo -e "\n$SUMMARY" >> "$MEMORY_FILE"
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
  echo -e "\n$SYS\n\nuser: $input" >> "$LOG_FILE"
  RESPONSE=$(openai api chat.completions.create -m gpt-4-turbo -p "$SYS\n\nuser: $input")
  echo -e "\nAssistant: $RESPONSE\n" >> "$LOG_FILE"
  echo "$RESPONSE"
}

# Handle interactive or single-prompt mode
if [ ${#PROMPTS[@]} -gt 0 ]; then
  for p in "${PROMPTS[@]}"; do
    call_ai "${p}"
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
EOF
chmod +x "$BASE_DIR/scripts/chat.sh"

# Copy global chat workflow doc into project root for easy access
cp CHAT_WORKFLOW.md "$BASE_DIR/CHAT_WORKFLOW.md"

echo "Project '$PROJECT_NAME' scaffolded at $BASE_DIR" 