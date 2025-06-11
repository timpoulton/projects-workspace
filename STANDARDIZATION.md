# Standardization Guidelines

This single document consolidates all project structure, deployment, and AI chat memory guidelines. It applies to every project under `projects/` in this repository.

## 1. Folder Structure

All projects must follow this layout at `projects/<project-name>/`:

- docs/        # Markdown documentation (archive, system master, memory, etc.)
- scripts/     # Utility scripts (e.g., chat.sh, health checks)
- src/         # Source code or application modules
- backups/     # Backup archives for data or configuration
- deploy/      # Deployment files (Dockerfile, docker-compose.yml, .env.example)
- `<Project> Master Document.md`
- `<Project> Memory.md`
- `<Project> Rules.md`

## 2. Governance Documents

- **Master Document**: High-level overview with objectives, stakeholders, deliverables, and timeline.
- **Memory File**: Project-specific memory (technical decisions, preferences) used to prime AI sessions.
- **Rules Document**: Project conventions (versioning, credentials, documentation standards).

## 3. Deployment (Docker)

- **Dockerfile**: Containerizes the application using a minimal base image.
- **docker-compose.yml**: Defines multi‐service setups and references `.env` for environment variables.
- **.env.example**: Template listing required environment variables. Copy to `.env` and fill in values.

## 4. AI Chat Wrapper

- **scripts/chat.sh**: Reads `<Project> Memory.md` and automatically sources `.env` before launching an AI chat session, ensuring every conversation starts with full project context.

## 5. Automated Scaffolding

- Use the provided `scripts/create-project.sh <project-name>` to scaffold new projects with the standard layout, Docker scaffolding, and governance docs.

## 6. Continuous Integration & Deployment

- Build Docker images in CI (e.g., GitHub Actions) to ensure consistent environments.
- Use `docker-compose` to bring up the application and any sidecar services for testing and production.

## 7. Updating Standardization

- This file is the single source of truth. When conventions evolve, update this document.
- Archive older standardization documents under `archive/standardization-old/` to preserve history.

## DNS Configuration

```dns-zone
;; Domain:     projekt-ai.net.
;; Exported:   2025-06-11 12:51:10
;;
;; This file is intended for use for informational and archival
;; purposes ONLY and MUST be edited before use on a production
;; DNS server.  In particular, you must:
;;   -- update the SOA record with the correct authoritative name server
;;   -- update the SOA record with the contact e-mail address information
;;   -- update the NS record(s) with the authoritative name servers for this domain.
;;
;; For further information, please consult the BIND documentation
;; located on the following website:
;;
;; http://www.isc.org/
;;
;; And RFC 1035:
;;
;; http://www.ietf.org/rfc/rfc1035.txt
;;
;; Please note that we do NOT offer technical support for any use
;; of this zone data, the BIND name server, or any other third-party
;; DNS software.
;;
;; Use at your own risk.
;; SOA Record
projekt-ai.net	3600	IN	SOA	eugene.ns.cloudflare.com. dns.cloudflare.com. 2050131287 10000 2400 604800 3600

;; NS Records
projekt-ai.net.	86400	IN	NS	eugene.ns.cloudflare.com.
projekt-ai.net.	86400	IN	NS	sue.ns.cloudflare.com.

;; A Records
api.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:false
blueprint.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
checkin.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
jellyfin.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
mail.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
n8n.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
nextcloud.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
projekt-ai.net.	1	IN	A	185.199.108.153 ; cf_tags=cf-proxied:true
projekt-ai.net.	1	IN	A	185.199.109.153 ; cf_tags=cf-proxied:true
projekt-ai.net.	1	IN	A	185.199.110.153 ; cf_tags=cf-proxied:true
projekt-ai.net.	1	IN	A	185.199.111.153 ; cf_tags=cf-proxied:true
proposals.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
qbittorrent.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
radarr.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
sonarr.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
test-api.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true
test-pages.projekt-ai.net.	1	IN	A	125.253.107.197 ; cf_tags=cf-proxied:true

;; CNAME Records
www.projekt-ai.net.	1	IN	CNAME	timpoulton.github.io. ; cf_tags=cf-proxied:false

;; MX Records
projekt-ai.net.	1	IN	MX	1 route3.mx.cloudflare.net.
projekt-ai.net.	1	IN	MX	60 route2.mx.cloudflare.net.
projekt-ai.net.	1	IN	MX	56 route1.mx.cloudflare.net.

;; TXT Records
_acme-challenge.projekt-ai.net.	1	IN	TXT	"A71koGR6Z_meInVwrsaGG0A26785X_FZOvuSL5qhnZc"
cf2024-1._domainkey.projekt-ai.net.	1	IN	TXT	"v=DKIM1; h=sha256; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiweykoi+o48IOGuP7GR3X0MOExCUDY/BCRHoWBnh3rChl7WhdyCxW3jgq1daEjPPqoi7sJvdg5hEQVsgVRQP4DcnQDVjGMbASQtrY4WmB1VebF+RPJB2ECPsEDTpeiI5ZyUAwJaVX7r6bznU67g7LvFq35yIo4sdlmtZGV+i0H4cpYH9+3JJ78k" "m4KXwaf9xUJCWF6nxeD+qG6Fyruw1Qlbds2r85U9dkNDVAS3gioCvELryh1TxKGiVTkg4wqHTyHfWsp7KD3WQHYJn0RyfJJu6YEmL77zonn7p2SRMvTMP3ZEXibnC9gz3nnhR6wcYL8Q7zXypKTMD58bTixDSJwIDAQAB"
projekt-ai.net.	1	IN	TXT	"v=spf1 include:_spf.mx.cloudflare.net ~all"
``` 