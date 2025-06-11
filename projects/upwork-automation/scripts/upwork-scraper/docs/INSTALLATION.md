# Installation Guide

This guide will help you set up the Upwork Scraper & Proposal Generator system on your machine.

## Prerequisites

- Python 3.8+
- Chrome browser (for Selenium)
- Git (optional, for cloning the repository)

## Installation Steps

### 1. Clone or Download the Repository

If you have Git installed:

```bash
git clone [repository-url]
cd upwork-scraper
```

Alternatively, download and extract the ZIP file from the repository.

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python packages:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### On Windows:
```bash
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the System

Copy the example configuration file and edit it with your settings:

```bash
cp src/config/config.example.py src/config/config.py
```

Edit `src/config/config.py` and update the following settings:

- `UPWORK_USERNAME`: Your Upwork username/email
- `UPWORK_PASSWORD`: Your Upwork password
- `CHROME_VERSIONS`: List of Chrome versions installed on your system
- `MULTIMODEL_SERVER`: URL of your Multi-Model AI server

### 6. Initialize the Database

```bash
python src/utils/init_db.py
```

### 7. Run the System

```bash
python scripts/run.py
```

The web interface will be available at http://localhost:5055 by default.

## Troubleshooting

### Chrome Version Issues

If you encounter issues with the Chrome driver, try:
1. Adding different Chrome versions to the `CHROME_VERSIONS` list in the config
2. Increasing the `MAX_ATTEMPTS` value in the config

### Upwork Login Issues

If you have issues logging into Upwork:
1. Ensure your credentials are correct
2. Check if your account requires 2FA and adjust settings accordingly
3. Make sure your UPWORK_USER_NAME matches the name displayed in your Upwork profile

### Multi-Model AI Server Connection

If the system can't connect to the Multi-Model AI server:
1. Ensure the server is running
2. Check that the URL in your config is correct
3. Verify network connectivity between the servers

## Next Steps

After installation, refer to the [User Guide](USER_GUIDE.md) for information on how to use the system. 