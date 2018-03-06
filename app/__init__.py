"""Initializes the application"""

from flask_api import FlaskAPI

from config import config

def create_app(configuration):
    """Set up and return app"""
    app = FlaskAPI(__name__)
    app.config.from_object(config[configuration])
    config[configuration].init_app(app)
    return app