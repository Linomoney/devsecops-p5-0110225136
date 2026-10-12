"""Penyimpanan in-memory untuk TaskTracker (cukup untuk demo/tugas kuliah)."""
from typing import Dict, List, Optional

from .models import Task
from .utils import generate_task_code


class TaskRepository:
    """Repository sederhana yang menyimpan tugas di dalam dictionary."""

    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add(self, **fields) -> Task:
        task = Task(task_id=self._next_id, code=generate_task_code(), **fields)
        self._tasks[task.task_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def list(self, status: Optional[str] = None) -> List[Task]:
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks

    def update(self, task_id: int, **fields) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        for key, value in fields.items():
            setattr(task, key, value)
        return task

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None
