"""
Unit tests untuk aplikasi TaskManager
"""
import pytest
from app import create_app
from app.config import TestingConfig
from app.database import db, Task, User
from app.services import TaskService, UserService


@pytest.fixture
def app():
    """Membuat instance aplikasi untuk testing."""
    application = create_app(TestingConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.drop_all()


@pytest.fixture
def client(app):
    """Membuat test client dari aplikasi."""
    return app.test_client()


# ─── Health Check Tests ───────────────────────────────────────────────────────

class TestHealthCheck:
    def test_health_endpoint_returns_200(self, client):
        """Memastikan endpoint health mengembalikan status 200."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self, client):
        """Memastikan endpoint health mengembalikan JSON yang valid."""
        response = client.get('/health')
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'service' in data


# ─── Task API Tests ───────────────────────────────────────────────────────────

class TestTaskAPI:
    def test_get_all_tasks_empty(self, client):
        """Memastikan endpoint GET /api/tasks/ mengembalikan list kosong."""
        response = client.get('/api/tasks/')
        assert response.status_code == 200
        assert response.get_json() == []

    def test_create_task_success(self, client):
        """Memastikan task baru dapat dibuat dengan data yang valid."""
        payload = {
            'title': 'Test Task',
            'description': 'Deskripsi test task',
            'priority': 'high'
        }
        response = client.post('/api/tasks/', json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Test Task'
        assert data['priority'] == 'high'
        assert data['status'] == 'pending'

    def test_create_task_without_title_fails(self, client):
        """Memastikan pembuatan task tanpa title menghasilkan error 400."""
        response = client.post('/api/tasks/', json={'description': 'no title'})
        assert response.status_code == 400

    def test_get_task_by_id(self, client):
        """Memastikan task dapat diambil berdasarkan ID."""
        create_response = client.post('/api/tasks/', json={'title': 'Find Me'})
        task_id = create_response.get_json()['id']

        response = client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        assert response.get_json()['title'] == 'Find Me'

    def test_get_nonexistent_task_returns_404(self, client):
        """Memastikan task yang tidak ada menghasilkan error 404."""
        response = client.get('/api/tasks/9999')
        assert response.status_code == 404

    def test_update_task_status(self, client):
        """Memastikan status task dapat diperbarui."""
        create_response = client.post('/api/tasks/', json={'title': 'Update Me'})
        task_id = create_response.get_json()['id']

        update_response = client.put(
            f'/api/tasks/{task_id}',
            json={'status': 'completed'}
        )
        assert update_response.status_code == 200
        assert update_response.get_json()['status'] == 'completed'

    def test_delete_task(self, client):
        """Memastikan task dapat dihapus."""
        create_response = client.post('/api/tasks/', json={'title': 'Delete Me'})
        task_id = create_response.get_json()['id']

        delete_response = client.delete(f'/api/tasks/{task_id}')
        assert delete_response.status_code == 200

        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404

    def test_filter_tasks_by_status(self, client):
        """Memastikan filter task berdasarkan status berfungsi."""
        client.post('/api/tasks/', json={'title': 'Task 1'})
        client.post('/api/tasks/', json={'title': 'Task 2'})

        task1_id = client.get('/api/tasks/').get_json()[0]['id']
        client.put(f'/api/tasks/{task1_id}', json={'status': 'completed'})

        response = client.get('/api/tasks/?status=completed')
        assert response.status_code == 200
        tasks = response.get_json()
        assert all(t['status'] == 'completed' for t in tasks)


# ─── Task Service Tests ───────────────────────────────────────────────────────

class TestTaskService:
    def test_create_task_via_service(self, app):
        """Memastikan TaskService.create menghasilkan objek Task yang valid."""
        with app.app_context():
            task = TaskService.create(
                title='Service Task',
                description='Dibuat via service',
                priority='low'
            )
            assert task.id is not None
            assert task.title == 'Service Task'
            assert task.status == 'pending'

    def test_get_summary(self, app):
        """Memastikan TaskService.get_summary mengembalikan statistik yang benar."""
        with app.app_context():
            TaskService.create(title='Task A')
            TaskService.create(title='Task B')
            summary = TaskService.get_summary()
            assert summary['total'] >= 2
            assert 'pending' in summary
            assert 'completed' in summary


# ─── User API Tests ───────────────────────────────────────────────────────────

class TestUserAPI:
    def test_create_user_success(self, client):
        """Memastikan user baru dapat dibuat."""
        payload = {'username': 'tengku', 'email': 'tengku@example.com'}
        response = client.post('/api/users/', json=payload)
        assert response.status_code == 201
        data = response.get_json()
        assert data['username'] == 'tengku'

    def test_create_duplicate_user_fails(self, client):
        """Memastikan username duplikat menghasilkan error 409."""
        payload = {'username': 'erlangga', 'email': 'erlangga@example.com'}
        client.post('/api/users/', json=payload)
        response = client.post(
            '/api/users/',
            json={'username': 'erlangga', 'email': 'other@example.com'}
        )
        assert response.status_code == 409

    def test_create_user_missing_fields(self, client):
        """Memastikan pembuatan user tanpa field wajib menghasilkan error 400."""
        response = client.post('/api/users/', json={'username': 'nomail'})
        assert response.status_code == 400
