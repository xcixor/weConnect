"""Initializes the application"""

from flask_api import FlaskAPI

from config import config

def create_app(configuration):
    """Set up and return app"""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config[configuration])
    config[configuration].init_app(app)

    from app.api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1')
    return app