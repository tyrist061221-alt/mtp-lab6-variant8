import unittest

from tasks.sredn_4_table_page import create_app


class TablePageTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_page_ok_and_has_table(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("<table", html)
        self.assertIn("Иванов Иван", html)

    def test_sort_by_grade_desc(self):
        html = self.client.get("/?sort=grade&order=desc").get_data(as_text=True)
        self.assertLess(html.index("Иванов Иван"), html.index("Сидоров Пётр"))

    def test_invalid_sort_falls_back(self):
        self.assertEqual(self.client.get("/?sort=hack").status_code, 200)


if __name__ == "__main__":
    unittest.main()
