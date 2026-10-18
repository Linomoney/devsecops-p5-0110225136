"""
Task Manager Application Package
Aplikasi manajemen tugas berbasis Flask REST API
"""

from flask import Flask
from .config import Config
from .database import db
from .routes import register_routes


def create_app(config_class=Config):
    """Application factory pattern untuk membuat Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inisialisasi database
    db.init_app(app)

    # Daftarkan semua routes
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
