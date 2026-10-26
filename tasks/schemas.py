"""Pydantic-схемы (Повыш.8): валидация входных и выходных данных.

Схемы используются во всех заданиях варианта:
  * FastAPI (Средн.8, Средн.10, Повыш.8) — тело запроса и response_model;
  * Flask + SQLite (Повыш.1) — валидация данных HTML-формы.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------- Средн.8: ответ на приветствие ----------
class Greeting(BaseModel):
    message: str
    name: str
    age: Optional[int] = None


# ---------- Средн.10 / Повыш.8: задачи ----------
class TaskCreate(BaseModel):
    """Данные для создания задачи."""
    title: str = Field(min_length=1, max_length=100, description="Название задачи")
    done: bool = False

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Название не может состоять из пробелов")
        return value


class TaskUpdate(BaseModel):
    """Частичное обновление задачи: все поля необязательные."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    done: Optional[bool] = None


class Task(TaskCreate):
    """Задача, как её видит клиент (с идентификатором)."""
    id: int


# ---------- Повыш.8: пользователи ----------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[A-Za-z0-9_]+$")
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    age: int = Field(ge=14, le=120)
    password: str = Field(min_length=6, max_length=64)


class UserOut(BaseModel):
    """Ответ без пароля — response_model скрывает лишние поля."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    age: int


# ---------- Повыш.1: заметки (Flask + SQLite) ----------
class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    text: str = Field(default="", max_length=2000)

    @field_validator("title", "text")
    @classmethod
    def strip_spaces(cls, value: str) -> str:
        return value.strip()

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("Заголовок не может быть пустым")
        return value


class NoteOut(NoteIn):
    id: int
    created_at: datetime
