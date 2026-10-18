"""
Business logic / service layer untuk aplikasi TaskManager
"""
from datetime import datetime
from .database import db, Task, User


class TaskService:
    """Service class yang menangani logika bisnis untuk entitas Task."""

    @staticmethod
    def get_all(status=None, priority=None):
        """Mengambil semua task dengan filter opsional."""
        query = Task.query
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        return query.order_by(Task.created_at.desc()).all()

    @staticmethod
    def get_by_id(task_id):
        """Mengambil task berdasarkan ID-nya."""
        return Task.query.get(task_id)

    @staticmethod
    def create(title, description=None, priority='medium', due_date=None):
        """Membuat task baru dan menyimpannya ke database."""
        parsed_due_date = None
        if due_date:
            try:
                parsed_due_date = datetime.fromisoformat(due_date)
            except ValueError:
                pass  # Abaikan format tanggal yang tidak valid

        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=parsed_due_date,
        )
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update(task, data):
        """Memperbarui field-field pada task yang sudah ada."""
        allowed_fields = ['title', 'description', 'status', 'priority']
        for field in allowed_fields:
            if field in data:
                setattr(task, field, data[field])

        if 'due_date' in data and data['due_date']:
            try:
                task.due_date = datetime.fromisoformat(data['due_date'])
            except ValueError:
                pass

        task.updated_at = datetime.utcnow()
        db.session.commit()
        return task

    @staticmethod
    def delete(task):
        """Menghapus task dari database."""
        db.session.delete(task)
        db.session.commit()

    @staticmethod
    def get_summary():
        """Mengambil ringkasan statistik task."""
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        completed = Task.query.filter_by(status='completed').count()
        return {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'completed': completed,
        }


class UserService:
    """Service class yang menangani logika bisnis untuk entitas User."""

    @staticmethod
    def get_all():
        """Mengambil semua pengguna aktif."""
        return User.query.filter_by(is_active=True).all()

    @staticmethod
    def get_by_id(user_id):
        """Mengambil pengguna berdasarkan ID."""
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username):
        """Mengambil pengguna berdasarkan username."""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create(username, email):
        """Membuat pengguna baru."""
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def deactivate(user):
        """Menonaktifkan akun pengguna (soft delete)."""
        user.is_active = False
        db.session.commit()
        return user
