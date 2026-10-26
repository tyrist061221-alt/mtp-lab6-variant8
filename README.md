# Лабораторная работа №6 — Веб-программирование на Python

**Говоруцкий Михаил Дмитриевич, группа 221141, вариант 8, лабораторная №6**

**Дисциплина:** «Методы и технологии программирования» (часть 1)

## Цель работы

Изучить основы веб-программирования: Flask и FastAPI, REST API, шаблоны Jinja2.

## Задания варианта 8

| Уровень    | № задания | Формулировка                      | Где реализовано                        |
|------------|-----------|-----------------------------------|----------------------------------------|
| Средний    | 8         | FastAPI принимает параметр и отвечает | `tasks/sredn_8_fastapi_param.py`   |
| Средний    | 10        | Простейший REST API список задач  | `tasks/sredn_10_todo_api.py`           |
| Средний    | 4         | Страница с таблицей данных        | `tasks/sredn_4_table_page.py`, `templates/table.html` |
| Повышенный | 8         | Использование Pydantic-схем       | `tasks/schemas.py`, `tasks/povysh_8_pydantic.py` |
| Повышенный | 1         | Flask с базой SQLite (CRUD)       | `tasks/povysh_1_flask_sqlite.py`, `templates/notes.html`, `templates/edit.html` |

## Структура проекта

```
mtp-lab6-variant8/
├── .github/workflows/ci.yml        # GitHub Actions: flake8 + unittest
├── main.py                         # справка по запуску заданий
├── requirements.txt
├── setup.cfg                       # настройки flake8
├── tasks/
│   ├── schemas.py                  # Pydantic-схемы (Повыш.8)
│   ├── sredn_8_fastapi_param.py
│   ├── sredn_10_todo_api.py
│   ├── sredn_4_table_page.py
│   ├── povysh_1_flask_sqlite.py
│   └── povysh_8_pydantic.py
├── templates/                      # шаблоны Jinja2
├── static/style.css
├── tests/                          # unittest
└── docs/INSTRUCTION_SUBMIT.md
```

## Установка и запуск

```
pip install -r requirements.txt

# Средн.8 — FastAPI с параметрами (Swagger: http://127.0.0.1:8000/docs)
uvicorn tasks.sredn_8_fastapi_param:app --reload
#   /hello/Миша      /greet?name=Миша&age=20

# Средн.10 — REST API задач
uvicorn tasks.sredn_10_todo_api:app --reload

# Средн.4 — таблица (Flask)
python -m tasks.sredn_4_table_page        # http://127.0.0.1:5000/

# Повыш.1 — Flask + SQLite (CRUD)
python -m tasks.povysh_1_flask_sqlite     # http://127.0.0.1:5000/

# Повыш.8 — Pydantic-схемы
uvicorn tasks.povysh_8_pydantic:app --reload
```

## Примеры REST API (Средн.10)

```
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title": "Сделать лабу"}'
curl http://127.0.0.1:8000/tasks
curl -X PUT http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -d '{"done": true}'
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Тесты и проверка стиля

```
python -m unittest discover -s tests -v
flake8 .
```
