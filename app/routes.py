"""Endpoint REST API untuk TaskTracker."""
from flask import Blueprint, current_app, jsonify, request

from .utils import summarize
from .validators import ValidationError, validate_task_payload

api = Blueprint("api", __name__)


def _repo():
    return current_app.extensions["task_repo"]


@api.get("/health")
def health():
    """Endpoint pengecekan kesehatan aplikasi."""
    return jsonify({"status": "ok"})


@api.get("/tasks")
def list_tasks():
    status = request.args.get("status")
    tasks = _repo().list(status=status)
    return jsonify([t.to_dict() for t in tasks])


@api.post("/tasks")
def create_task():
    try:
        data = validate_task_payload(request.get_json(silent=True))
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    task = _repo().add(**data)
    return jsonify(task.to_dict()), 201


@api.get("/tasks/<int:task_id>")
def get_task(task_id: int):
    task = _repo().get(task_id)
    if task is None:
        return jsonify({"error": "Tugas tidak ditemukan."}), 404
    return jsonify(task.to_dict())


@api.put("/tasks/<int:task_id>")
def update_task(task_id: int):
    try:
        data = validate_task_payload(request.get_json(silent=True), partial=True)
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400
    task = _repo().update(task_id, **data)
    if task is None:
        return jsonify({"error": "Tugas tidak ditemukan."}), 404
    return jsonify(task.to_dict())


@api.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    if not _repo().delete(task_id):
        return jsonify({"error": "Tugas tidak ditemukan."}), 404
    return "", 204


@api.get("/summary")
def summary():
    return jsonify(summarize(_repo().list()))
