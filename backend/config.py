"""Configuration settings for the application"""
import os


class Config:
    """Base configuration"""
    DATABASE = os.environ.get('DATABASE', 'social_media.db')
    TESTING = False
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE = 'test_social_media.db'


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
