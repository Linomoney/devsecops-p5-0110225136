"""TaskTracker - aplikasi manajemen tugas sederhana berbasis Flask."""
from flask import Flask

from .routes import api
from .storage import TaskRepository


def create_app() -> Flask:
    """Application factory: membuat dan mengonfigurasi instance Flask."""
    application = Flask(__name__)
    application.extensions["task_repo"] = TaskRepository()
    application.register_blueprint(api)
    return application
