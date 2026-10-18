"""
Konfigurasi aplikasi TaskManager
"""
import os


class Config:
    """Konfigurasi default aplikasi."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-ganti-di-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///tasks.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Konfigurasi untuk environment development."""
    DEBUG = True


class TestingConfig(Config):
    """Konfigurasi untuk environment testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'


class ProductionConfig(Config):
    """Konfigurasi untuk environment production."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Wajib diset di env production


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
