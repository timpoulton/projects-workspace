# Projects Rules
+Please refer to `/STANDARDIZATION.md` for the complete unified standardization guidelines for all projects.

1. Whenever a new project folder is created, it must include:
   - Master Document
   - Memory File
   - Rules Document
   - deploy/ directory containing:
     - Dockerfile (to containerize the application)
     - docker-compose.yml (to define multi‐service setup)
     - .env.example (template for environment variables)
   - scripts/chat.sh: Chat wrapper script that loads the project's Memory file into the AI as a system prompt.
