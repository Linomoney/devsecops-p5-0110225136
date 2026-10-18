"""
Model database untuk aplikasi TaskManager
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    """Model untuk entitas Task (tugas)."""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20),
        nullable=False,
        default='pending'
    )  # pending, in_progress, completed
    priority = db.Column(
        db.String(10),
        nullable=False,
        default='medium'
    )  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    due_date = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        """Konversi model ke dictionary untuk serialisasi JSON."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
        }

    def __repr__(self):
        return f'<Task {self.id}: {self.title} [{self.status}]>'


class User(db.Model):
    """Model untuk entitas User (pengguna)."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        """Konversi model ke dictionary untuk serialisasi JSON."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
        }

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'
