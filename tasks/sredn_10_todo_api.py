"""Средн.10 — простейший REST API «список задач» (FastAPI).

Запуск:  uvicorn tasks.sredn_10_todo_api:app --reload
Swagger: http://127.0.0.1:8000/docs

Метод      URL            Действие
GET        /tasks         список задач
GET        /tasks/{id}    одна задача
POST       /tasks         создать (201)
PUT        /tasks/{id}    обновить
DELETE     /tasks/{id}    удалить (204)
"""
from typing import Dict, List

from fastapi import FastAPI, HTTPException, Response, status

from tasks.schemas import Task, TaskCreate, TaskUpdate


def create_app() -> FastAPI:
    """Фабрика приложения: у каждого экземпляра своё хранилище (удобно для тестов)."""
    api = FastAPI(title="Средн.10 — REST API списка задач", version="1.0.0")
    storage: Dict[int, Task] = {}
    counter = {"next_id": 1}

    def get_or_404(task_id: int) -> Task:
        task = storage.get(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return task

    @api.get("/tasks", response_model=List[Task])
    def list_tasks() -> List[Task]:
        return list(storage.values())

    @api.get("/tasks/{task_id}", response_model=Task)
    def get_task(task_id: int) -> Task:
        return get_or_404(task_id)

    @api.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
    def create_task(data: TaskCreate) -> Task:
        task = Task(id=counter["next_id"], **data.model_dump())
        storage[task.id] = task
        counter["next_id"] += 1
        return task

    @api.put("/tasks/{task_id}", response_model=Task)
    def update_task(task_id: int, data: TaskUpdate) -> Task:
        task = get_or_404(task_id)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        updated = task.model_copy(update=changes)
        storage[task_id] = updated
        return updated

    @api.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_task(task_id: int) -> Response:
        get_or_404(task_id)
        del storage[task_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return api


app = create_app()
