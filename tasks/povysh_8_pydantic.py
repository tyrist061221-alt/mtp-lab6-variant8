"""Повыш.8 — использование Pydantic-схем (FastAPI).

Показано:
  * валидация тела запроса (UserCreate: длина, regex, диапазон возраста);
  * response_model=UserOut — пароль никогда не попадает в ответ;
  * автоматический ответ 422 при ошибке валидации;
  * схемы отражаются в Swagger (/docs).

Запуск:  uvicorn tasks.povysh_8_pydantic:app --reload
"""
from typing import Dict, List

from fastapi import FastAPI, HTTPException, status

from tasks.schemas import UserCreate, UserOut


def create_app() -> FastAPI:
    api = FastAPI(title="Повыш.8 — Pydantic-схемы", version="1.0.0")
    users: Dict[int, dict] = {}
    counter = {"next_id": 1}

    @api.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
    def register(data: UserCreate) -> dict:
        if any(u["username"].lower() == data.username.lower() for u in users.values()):
            raise HTTPException(status_code=409, detail="Пользователь уже существует")
        user = {"id": counter["next_id"], **data.model_dump()}
        users[user["id"]] = user
        counter["next_id"] += 1
        return user  # поле password отфильтрует response_model

    @api.get("/users", response_model=List[UserOut])
    def list_users() -> List[dict]:
        return list(users.values())

    @api.get("/users/{user_id}", response_model=UserOut)
    def get_user(user_id: int) -> dict:
        if user_id not in users:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return users[user_id]

    return api


app = create_app()
