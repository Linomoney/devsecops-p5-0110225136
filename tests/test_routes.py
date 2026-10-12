import unittest

from app import create_app


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"status": "ok"})

    def test_create_and_get_task(self):
        res = self.client.post("/tasks", json={"title": "Setup pipeline"})
        self.assertEqual(res.status_code, 201)
        task_id = res.get_json()["task_id"]
        res = self.client.get(f"/tasks/{task_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["title"], "Setup pipeline")

    def test_create_invalid(self):
        self.assertEqual(self.client.post("/tasks", json={"title": ""}).status_code, 400)

    def test_get_not_found(self):
        self.assertEqual(self.client.get("/tasks/42").status_code, 404)

    def test_update_task(self):
        tid = self.client.post("/tasks", json={"title": "A"}).get_json()["task_id"]
        res = self.client.put(f"/tasks/{tid}", json={"status": "done"})
        self.assertEqual(res.get_json()["status"], "done")
        self.assertEqual(
            self.client.put("/tasks/99", json={"status": "done"}).status_code, 404
        )
        self.assertEqual(
            self.client.put(f"/tasks/{tid}", json={"status": "x"}).status_code, 400
        )

    def test_delete_task(self):
        tid = self.client.post("/tasks", json={"title": "A"}).get_json()["task_id"]
        self.assertEqual(self.client.delete(f"/tasks/{tid}").status_code, 204)
        self.assertEqual(self.client.delete(f"/tasks/{tid}").status_code, 404)

    def test_list_and_summary(self):
        self.client.post("/tasks", json={"title": "A"})
        self.client.post("/tasks", json={"title": "B", "status": "done"})
        self.assertEqual(len(self.client.get("/tasks").get_json()), 2)
        self.assertEqual(len(self.client.get("/tasks?status=done").get_json()), 1)
        summary = self.client.get("/summary").get_json()
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["done"], 1)


if __name__ == "__main__":
    unittest.main()
