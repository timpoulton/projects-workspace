# Upwork Scraper & Proposal Generator

## Overview

This project is an integrated system for:
1. Searching and scraping Upwork jobs
2. Managing job listings
3. Generating high-quality proposals using multi-model AI

The system allows users to manually search for jobs on Upwork, review results, and generate customized proposals with a single click. It eliminates the complexity of the previous automation system while maintaining the quality of AI-generated proposals.

## Key Features

- **Job Search Interface** - Search Upwork jobs with custom queries
- **Built-in Scraper** - Uses Selenium with undetected ChromeDriver to bypass Upwork anti-scraping
- **Job Management** - Review, approve, or reject jobs from the search results
- **Multi-Model AI Integration** - Generate high-quality proposals using existing AI infrastructure
- **Dark Theme UI** - Professional dark-themed interface for the proposal generator

## Architecture

The project follows a modular design with clear separation of concerns:

```
upwork-scraper/
├── docs/             # Documentation files
├── scripts/          # Utility scripts for installation and running
└── src/              # Source code
    ├── api/          # API endpoints for the web interface
    ├── config/       # Configuration files
    ├── models/       # Data models
    ├── scraper/      # Upwork scraping functionality
    ├── tests/        # Test cases
    ├── ui/           # Web interface templates and assets
    └── utils/        # Utility functions
```

## Technical Stack

- **Backend**: Python with Flask
- **Database**: SQLite
- **Web Scraping**: Selenium with undetected ChromeDriver
- **AI Models**: Integration with existing multi-model AI system
- **Frontend**: HTML, CSS, JavaScript with dark theme

## Getting Started

Please see the [installation guide](docs/INSTALLATION.md) for setup instructions and the [user guide](docs/USER_GUIDE.md) for usage information.

## Development

For information on project structure, coding standards, and how to contribute, please see the [development guide](docs/DEVELOPMENT.md).

## Project Status

This project is currently in active development.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 