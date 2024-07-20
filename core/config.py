import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///./store.sqlite3')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///./dev.sqlite3')

class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///./test.sqlite3')
    DEBUG = False  # Typically, DEBUG is False in testing environment

class ProductionConfig(Config):
    """Configuration for production environment."""
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL', 'sqlite:///./prod.sqlite3')
