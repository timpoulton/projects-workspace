# Backend Setup Record

This document summarizes all the backend and CI/CD configuration tasks we've applied across the repository:

- Created `STANDARDIZATION.md` at repo root, consolidating project structure, Docker deployment, and AI chat memory guidelines.
- Archived legacy standardization docs under `homelab-docs/archive/standardization-old/`.
- Updated `projects/Projects Rules.md` to reference `STANDARDIZATION.md`.
- Added `scripts/create-project.sh` to scaffold new projects with:
  - Standard folder layout (`docs/`, `scripts/`, `src/`, `backups/`, `deploy/`)
  - Governance docs (`Master`, `Memory`, `Rules` files)
  - Docker scaffolding (`Dockerfile`, `docker-compose.yml`, `.env.example`)
  - Fully automated `scripts/chat.sh` with `--resume`, `--update-memory`, `--workflow` flags, logging & memory auto-update
  - Copied `CHAT_WORKFLOW.md` into each project
- Migrated and containerized key projects:
  1. **projects/upwork-automation**
  2. **projects/club77-guestlist**
  3. **projects/projekt-ai-website**
- For `projekt-ai-website`:
  - Converted Dockerfile to multi-stage Node.js → Nginx build
  - Updated `docker-compose.yml`: removed `version`, added healthcheck
  - Moved and updated `netlify.toml` to repo root with `build.base` pointing to the subfolder
- Created `CHAT_WORKFLOW.md` with step-by-step instructions and integrated it into the chat wrappers
- Added GitHub Actions workflow (`.github/workflows/ci.yml`) to:
  - Install dependencies (Python and Node)
  - Build each project
  - Build and health-check Docker images

Commit and push to activate CI, Netlify, and containerized deployments. 