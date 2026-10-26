import unittest

try:
    from fastapi.testclient import TestClient

    from tasks.povysh_8_pydantic import create_app as create_users_app
    from tasks.sredn_10_todo_api import create_app as create_todo_app
    from tasks.sredn_8_fastapi_param import app as param_app
except ImportError:  # fastapi/httpx не установлены
    TestClient = None


@unittest.skipIf(TestClient is None, "fastapi/httpx не установлены")
class ParamTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(param_app)

    def test_root(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_path_param(self):
        data = self.client.get("/hello/Миша").json()
        self.assertEqual(data["message"], "Привет, Миша!")

    def test_query_param(self):
        data = self.client.get("/greet", params={"name": "Анна", "age": 20}).json()
        self.assertIn("Анна", data["message"])
        self.assertEqual(data["age"], 20)

    def test_query_default(self):
        self.assertEqual(self.client.get("/greet").json()["name"], "гость")

    def test_query_validation(self):
        self.assertEqual(self.client.get("/greet", params={"age": -5}).status_code, 422)


@unittest.skipIf(TestClient is None, "fastapi/httpx не установлены")
class TodoApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_todo_app())

    def test_full_cycle(self):
        resp = self.client.post("/tasks", json={"title": "Сделать лабу"})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json(), {"id": 1, "title": "Сделать лабу", "done": False})
        self.assertEqual(len(self.client.get("/tasks").json()), 1)
        upd = self.client.put("/tasks/1", json={"done": True})
        self.assertTrue(upd.json()["done"])
        self.assertEqual(self.client.get("/tasks/1").status_code, 200)
        self.assertEqual(self.client.delete("/tasks/1").status_code, 204)
        self.assertEqual(self.client.get("/tasks/1").status_code, 404)

    def test_validation(self):
        self.assertEqual(self.client.post("/tasks", json={"title": ""}).status_code, 422)
        self.assertEqual(self.client.post("/tasks", json={}).status_code, 422)

    def test_404(self):
        self.assertEqual(self.client.put("/tasks/5", json={"done": True}).status_code, 404)
        self.assertEqual(self.client.delete("/tasks/5").status_code, 404)


@unittest.skipIf(TestClient is None, "fastapi/httpx не установлены")
class PydanticUsersTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_users_app())
        self.valid = {"username": "misha_01", "email": "m@example.com",
                      "age": 20, "password": "secret1"}

    def test_password_hidden(self):
        resp = self.client.post("/users", json=self.valid)
        self.assertEqual(resp.status_code, 201)
        self.assertNotIn("password", resp.json())

    def test_invalid_data(self):
        for field, value in [("username", "a"), ("email", "bad"), ("age", 5),
                             ("password", "123")]:
            payload = dict(self.valid, **{field: value})
            self.assertEqual(self.client.post("/users", json=payload).status_code, 422, field)

    def test_duplicate(self):
        self.client.post("/users", json=self.valid)
        self.assertEqual(self.client.post("/users", json=self.valid).status_code, 409)


if __name__ == "__main__":
    unittest.main()
