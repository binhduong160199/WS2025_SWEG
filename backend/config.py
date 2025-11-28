"""Configuration settings for the application"""
import os



class Config:
    """Base configuration"""
    # Use DATABASE_URL for SQLAlchemy/PostgreSQL
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/social_media')
    TESTING = False
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True



class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/test_social_media')


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
