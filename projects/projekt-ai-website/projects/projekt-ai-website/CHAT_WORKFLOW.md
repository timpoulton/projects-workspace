# AI Chat Workflow

A simple, 3-phase guide to using AI chat in your projects.

## 1. Start a New Session
1. Change to your project directory:
   ```bash
   cd projects/<project-name>
   ```
2. Ensure your environment variables are set:
   ```bash
   cp deploy/.env.example deploy/.env  # if first time
   # fill in deploy/.env with your API key etc.
   ```
3. Launch the chat wrapper:
   ```bash
   ./scripts/chat.sh
   ```

## 2. During the Chat
- **Ask questions** as usual; context from `<Project> Memory.md` is loaded automatically.
- To **resume** after a disconnect or token limit:
   ```bash
   ./scripts/chat.sh --resume
   ```
- To **append** a note into memory on-the-fly:
   ```bash
   ./scripts/chat.sh --update-memory
   ```
- To get a memory snippet for manual addition, prefix notes in chat with:
   ```
   NOTE_FOR_MEMORY: <your note here>
   ```
  then paste the snippet from the AI's response into `<Project> Memory.md`.

## 3. End of Session
1. (Optional) View the log in `logs/chat-<timestamp>.log` for full history.
2. Commit any updates to `<Project> Memory.md` in Git:
   ```bash
   git add "<Project> Memory.md"
   git commit -m "Update project memory"
   ```
3. Start your next chat whenever you need—your memory is always loaded fresh.

## Workflow Mode

At any point, you can enter "workflow mode" to view these instructions:

- From a new shell:
  ```bash
  ./scripts/chat.sh --workflow
  ```
- During an interactive chat session, type:
  ```text
  enter workflow mode
  ```
  This will re-display this workflow. 