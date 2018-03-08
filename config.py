"""Contains app configurations"""

import os

class Config:
    """
    Contains the common setings that all configuration options must have
    """
    Debug = False
    SECRET_KEY = os.urandom(30)

    @staticmethod
    def init_app(app):
        """
        To perform configuration specific initializations
        """
        pass

class Development(Config):
    """
    Configurations used by developer
    """
    DEBUG = True

class Testing(Config):
    """
    Configurations used for testing
    """
    TESTING = True


class Production(Config):
    """
    Configurations used after product release
    """
    DEBUG = False
    
#Registers tconfigurations
config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}