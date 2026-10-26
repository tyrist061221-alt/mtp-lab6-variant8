import os
import tempfile
import unittest

try:
    from tasks.povysh_1_flask_sqlite import create_app
except ImportError:  # pydantic не установлен
    create_app = None


@unittest.skipIf(create_app is None, "pydantic/flask не установлены")
class NotesCrudTests(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        self.client = create_app(self.db_path).test_client()

    def tearDown(self):
        os.remove(self.db_path)

    def add(self, title="Заметка", text="Текст"):
        return self.client.post("/add", data={"title": title, "text": text})

    def test_create_and_read(self):
        self.assertEqual(self.add().status_code, 302)
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("Заметка", html)

    def test_validation_error(self):
        resp = self.add(title="   ")
        self.assertEqual(resp.status_code, 400)

    def test_update(self):
        self.add()
        resp = self.client.post("/edit/1", data={"title": "Новая", "text": "x"})
        self.assertEqual(resp.status_code, 302)
        self.assertIn("Новая", self.client.get("/").get_data(as_text=True))

    def test_delete(self):
        self.add()
        self.assertEqual(self.client.post("/delete/1").status_code, 302)
        self.assertNotIn("Заметка", self.client.get("/").get_data(as_text=True))

    def test_404(self):
        self.assertEqual(self.client.get("/edit/999").status_code, 404)
        self.assertEqual(self.client.post("/delete/999").status_code, 404)


if __name__ == "__main__":
    unittest.main()
