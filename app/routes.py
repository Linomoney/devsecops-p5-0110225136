"""
Routes / endpoint API untuk aplikasi TaskManager
"""
from flask import Blueprint, request, jsonify
from .database import db, Task, User
from .services import TaskService, UserService

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')
users_bp = Blueprint('users', __name__, url_prefix='/api/users')
health_bp = Blueprint('health', __name__)


def register_routes(app):
    """Mendaftarkan semua blueprint ke aplikasi Flask."""
    app.register_blueprint(tasks_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(health_bp)


# ─── Health Check ────────────────────────────────────────────────────────────

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint health check untuk memastikan aplikasi berjalan."""
    return jsonify({'status': 'healthy', 'service': 'TaskManager API'}), 200


# ─── Task Endpoints ───────────────────────────────────────────────────────────

@tasks_bp.route('/', methods=['GET'])
def get_all_tasks():
    """Mengambil semua task, dengan dukungan filter status dan priority."""
    status = request.args.get('status')
    priority = request.args.get('priority')
    tasks = TaskService.get_all(status=status, priority=priority)
    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Mengambil satu task berdasarkan ID."""
    task = TaskService.get_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task tidak ditemukan'}), 404
    return jsonify(task.to_dict()), 200


@tasks_bp.route('/', methods=['POST'])
def create_task():
    """Membuat task baru."""
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Field title wajib diisi'}), 400

    task = TaskService.create(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        due_date=data.get('due_date'),
    )
    return jsonify(task.to_dict()), 201


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Memperbarui task yang sudah ada."""
    task = TaskService.get_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task tidak ditemukan'}), 404

    data = request.get_json()
    task = TaskService.update(task, data)
    return jsonify(task.to_dict()), 200


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Menghapus task berdasarkan ID."""
    task = TaskService.get_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task tidak ditemukan'}), 404

    TaskService.delete(task)
    return jsonify({'message': 'Task berhasil dihapus'}), 200


# ─── User Endpoints ───────────────────────────────────────────────────────────

@users_bp.route('/', methods=['GET'])
def get_all_users():
    """Mengambil semua pengguna."""
    users = UserService.get_all()
    return jsonify([u.to_dict() for u in users]), 200


@users_bp.route('/', methods=['POST'])
def create_user():
    """Membuat pengguna baru."""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Field username dan email wajib diisi'}), 400

    existing = UserService.get_by_username(data['username'])
    if existing:
        return jsonify({'error': 'Username sudah digunakan'}), 409

    user = UserService.create(
        username=data['username'],
        email=data['email']
    )
    return jsonify(user.to_dict()), 201
