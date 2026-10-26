"""Средн.4 — страница с таблицей данных (Flask + Jinja2).

Запуск:  python -m tasks.sredn_4_table_page   ->  http://127.0.0.1:5000/
Сортировка: /?sort=grade&order=desc
"""
from pathlib import Path

from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent.parent

STUDENTS = [
    {"id": 1, "name": "Иванов Иван", "group": "221141", "grade": 5},
    {"id": 2, "name": "Петрова Анна", "group": "221141", "grade": 4},
    {"id": 3, "name": "Сидоров Пётр", "group": "221142", "grade": 3},
    {"id": 4, "name": "Кузнецова Мария", "group": "221142", "grade": 5},
    {"id": 5, "name": "Смирнов Алексей", "group": "221143", "grade": 4},
]
SORT_FIELDS = {"id", "name", "group", "grade"}


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    @app.route("/")
    def table():
        sort = request.args.get("sort", "id")
        if sort not in SORT_FIELDS:
            sort = "id"
        reverse = request.args.get("order", "asc") == "desc"
        rows = sorted(STUDENTS, key=lambda s: s[sort], reverse=reverse)
        average = sum(s["grade"] for s in rows) / len(rows)
        return render_template(
            "table.html", rows=rows, sort=sort, reverse=reverse, average=average
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
