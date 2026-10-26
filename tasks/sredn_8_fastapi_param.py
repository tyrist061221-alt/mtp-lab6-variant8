"""Средн.8 — FastAPI принимает параметр и отвечает.

Запуск:  uvicorn tasks.sredn_8_fastapi_param:app --reload
Swagger: http://127.0.0.1:8000/docs
"""
from typing import Optional

from fastapi import FastAPI, Query

from tasks.schemas import Greeting

app = FastAPI(title="Средн.8 — параметры в FastAPI", version="1.0.0")


@app.get("/")
def root() -> dict:
    return {"message": "Привет, FastAPI!"}


@app.get("/hello/{name}", response_model=Greeting)
def hello_path(name: str) -> Greeting:
    """Параметр пути: GET /hello/Миша."""
    return Greeting(message=f"Привет, {name}!", name=name)


@app.get("/greet", response_model=Greeting)
def greet_query(
    name: str = Query(default="гость", min_length=1, max_length=50),
    age: Optional[int] = Query(default=None, ge=0, le=150),
) -> Greeting:
    """Query-параметры: GET /greet?name=Миша&age=20."""
    text = f"Привет, {name}!"
    if age is not None:
        text += f" Тебе {age}."
    return Greeting(message=text, name=name, age=age)
