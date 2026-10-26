"""Лабораторная работа №6 — Веб-программирование на Python (вариант 8).

Справка по запуску всех заданий варианта.
"""

TASKS = [
    ("Средн.8", "FastAPI принимает параметр и отвечает",
     "uvicorn tasks.sredn_8_fastapi_param:app --reload"),
    ("Средн.10", "Простейший REST API список задач",
     "uvicorn tasks.sredn_10_todo_api:app --reload"),
    ("Средн.4", "Страница с таблицей данных (Flask + Jinja2)",
     "python -m tasks.sredn_4_table_page"),
    ("Повыш.1", "Flask с базой SQLite (CRUD)",
     "python -m tasks.povysh_1_flask_sqlite"),
    ("Повыш.8", "Использование Pydantic-схем",
     "uvicorn tasks.povysh_8_pydantic:app --reload"),
]


def main() -> None:
    print("Лабораторная №6, вариант 8. Команды запуска:\n")
    for code, title, cmd in TASKS:
        print(f"[{code}] {title}\n    {cmd}\n")


if __name__ == "__main__":
    main()
