# Development Guide

This guide provides information for developers who want to understand, modify, or contribute to the Upwork Scraper & Proposal Generator.

## Project Structure

The project follows a modular architecture with clear separation of concerns:

```
upwork-scraper/
├── docs/             # Documentation files
│   ├── INSTALLATION.md
│   ├── USER_GUIDE.md
│   └── DEVELOPMENT.md
├── scripts/          # Utility scripts
│   ├── run.py
│   └── init_db.py
├── src/              # Source code
│   ├── api/          # API endpoints
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── endpoints/
│   ├── config/       # Configuration
│   │   ├── __init__.py
│   │   ├── config.example.py
│   │   └── config.py
│   ├── models/       # Data models
│   │   ├── __init__.py
│   │   ├── job.py
│   │   └── proposal.py
│   ├── scraper/      # Upwork scraping
│   │   ├── __init__.py
│   │   ├── upwork_login.py
│   │   ├── upwork_scraper.py
│   │   └── job_parser.py
│   ├── tests/        # Test cases
│   │   ├── __init__.py
│   │   ├── test_scraper.py
│   │   └── test_api.py
│   ├── ui/           # UI assets
│   │   ├── static/
│   │   └── templates/
│   └── utils/        # Utilities
│       ├── __init__.py
│       ├── db.py
│       └── helpers.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Key Components

### 1. Web Interface (`src/api`)

A Flask-based web application that provides:
- Search interface for Upwork jobs
- Job management (viewing, approving, rejecting)
- Proposal generation requests
- Result display

### 2. Scraper (`src/scraper`)

The core job scraping functionality:
- Upwork login management
- Job search navigation
- Result extraction
- Anti-detection measures

### 3. Models (`src/models`)

Data models for:
- Jobs (title, description, budget, etc.)
- Proposals (content, status, timestamp)
- User preferences

### 4. AI Integration (`src/api/endpoints`)

Communicates with the existing Multi-Model AI server:
- Formats job data for AI processing
- Sends requests to generate proposals
- Processes and formats responses

## Development Workflow

### Setting Up Development Environment

1. Follow the [installation guide](INSTALLATION.md)
2. Install additional development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running Tests

```bash
pytest src/tests/
```

### Code Style

This project follows PEP 8 style guidelines. Use the following tools to maintain code quality:

```bash
# Format code
black src/

# Check style
flake8 src/

# Run type checking
mypy src/
```

### Adding New Features

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement Your Changes**:
   - Add necessary files to appropriate directories
   - Update documentation as needed
   - Add tests for new functionality

3. **Test Your Changes**:
   ```bash
   pytest src/tests/
   ```

4. **Submit a Pull Request**:
   - Provide a clear description of your changes
   - Reference any related issues

## Extending the System

### Adding New Scraper Features

To add new scraping capabilities:
1. Extend the scraper classes in `src/scraper/`
2. Update job parsing in `src/scraper/job_parser.py`
3. Add UI elements in `src/ui/templates/`

### Customizing Proposal Generation

To modify how proposals are generated:
1. Update the API endpoints in `src/api/endpoints/`
2. Modify the request format to the Multi-Model AI server

### Adding New UI Features

1. Add new routes in `src/api/routes.py`
2. Create new templates in `src/ui/templates/`
3. Add static assets in `src/ui/static/`

## Database Schema

The system uses SQLite with the following main tables:

### Jobs Table
- `id`: Unique identifier
- `job_id`: Upwork job ID
- `title`: Job title
- `description`: Full job description
- `budget`: Job budget
- `client_name`: Client name
- `url`: Job URL
- `created_at`: Timestamp when job was scraped
- `status`: Status (pending, approved, rejected)

### Proposals Table
- `id`: Unique identifier
- `job_id`: Reference to Jobs table
- `content`: Generated proposal content
- `created_at`: Timestamp when proposal was generated
- `score`: Match score

## Integration Points

### Multi-Model AI Server

The system integrates with the existing Multi-Model AI server via HTTP:
- Endpoint: `http://localhost:5001/webhook/job-direct`
- Request format: JSON with job details
- Response format: JSON with proposal data

## Troubleshooting Development Issues

- **Chrome Driver Issues**: See the troubleshooting section in the [Installation Guide](INSTALLATION.md)
- **Database Errors**: Check file permissions and SQLite version
- **UI Issues**: Check browser console for JavaScript errors

## Deployment Considerations

For production deployment:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up proper authentication
3. Configure proper logging
4. Use environment variables for sensitive configuration 