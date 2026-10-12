import re
import unittest

from app.models import Task
from app.utils import generate_task_code, summarize


class ModelTests(unittest.TestCase):
    def test_task_defaults(self):
        task = Task(task_id=1, code="TK-AAAAAA", title="Belajar CI")
        self.assertEqual(task.status, "todo")
        self.assertEqual(task.priority, "medium")
        self.assertFalse(task.is_finished())

    def test_task_finished_and_dict(self):
        task = Task(task_id=2, code="TK-BBBBBB", title="Selesai", status="done")
        self.assertTrue(task.is_finished())
        self.assertEqual(task.to_dict()["title"], "Selesai")


class UtilsTests(unittest.TestCase):
    def test_generate_task_code_format(self):
        self.assertRegex(generate_task_code(), r"^TK-[A-Z0-9]{6}$")

    def test_generate_task_code_length(self):
        self.assertTrue(re.fullmatch(r"TK-[A-Z0-9]{10}", generate_task_code(10)))

    def test_summarize(self):
        tasks = [
            Task(1, "TK-1", "a", status="todo"),
            Task(2, "TK-2", "b", status="done"),
            Task(3, "TK-3", "c", status="done"),
        ]
        self.assertEqual(
            summarize(tasks), {"total": 3, "todo": 1, "in_progress": 0, "done": 2}
        )


if __name__ == "__main__":
    unittest.main()
