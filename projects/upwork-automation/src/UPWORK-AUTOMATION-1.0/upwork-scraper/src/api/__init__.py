"""
API module for the Upwork Scraper & Proposal Generator
"""

from flask import Flask
from flask_cors import CORS

def create_app():
    """
    Create and configure the Flask application
    """
    app = Flask(__name__, 
                template_folder='../ui/templates', 
                static_folder='../ui/static')
    
    # Enable CORS
    CORS(app)
    
    # Load configuration
    try:
        from config import config
        app.config.from_object(config)
        app.secret_key = getattr(config, 'SECRET_KEY', 'dev-key-change-this')
    except ImportError:
        app.logger.warning("Config module not found. Using default configuration.")
        app.config.from_mapping(
            SECRET_KEY='dev-key-change-this',
            DATABASE_PATH='upwork_scraper.db',
            MULTIMODEL_SERVER='http://localhost:5001'
        )
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # Initialize database
    from utils.db import init_app_db
    init_app_db(app)
    
    return app 