import unittest

from app.storage import TaskRepository
from app.validators import ValidationError, validate_task_payload


class ValidatorTests(unittest.TestCase):
    def test_valid_payload(self):
        data = validate_task_payload({"title": "  Tulis laporan  ", "priority": "high"})
        self.assertEqual(data, {"title": "Tulis laporan", "priority": "high"})

    def test_missing_title(self):
        with self.assertRaises(ValidationError):
            validate_task_payload({"description": "tanpa judul"})

    def test_title_too_long(self):
        with self.assertRaises(ValidationError):
            validate_task_payload({"title": "x" * 101})

    def test_invalid_status_and_priority(self):
        with self.assertRaises(ValidationError):
            validate_task_payload({"title": "a", "status": "selesai"})
        with self.assertRaises(ValidationError):
            validate_task_payload({"title": "a", "priority": "urgent"})

    def test_description_rules(self):
        with self.assertRaises(ValidationError):
            validate_task_payload({"title": "a", "description": 123})
        with self.assertRaises(ValidationError):
            validate_task_payload({"title": "a", "description": "x" * 501})

    def test_non_dict_payload(self):
        with self.assertRaises(ValidationError):
            validate_task_payload(["bukan", "dict"])

    def test_partial_update_allows_missing_title(self):
        self.assertEqual(
            validate_task_payload({"status": "done"}, partial=True), {"status": "done"}
        )


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repo = TaskRepository()

    def test_add_get_list(self):
        t = self.repo.add(title="Satu")
        self.assertEqual(self.repo.get(t.task_id).title, "Satu")
        self.assertEqual(len(self.repo.list()), 1)

    def test_filter_by_status(self):
        self.repo.add(title="A")
        self.repo.add(title="B", status="done")
        self.assertEqual(len(self.repo.list(status="done")), 1)

    def test_update_and_delete(self):
        t = self.repo.add(title="A")
        self.assertEqual(self.repo.update(t.task_id, status="done").status, "done")
        self.assertIsNone(self.repo.update(999, status="done"))
        self.assertTrue(self.repo.delete(t.task_id))
        self.assertFalse(self.repo.delete(t.task_id))


if __name__ == "__main__":
    unittest.main()
