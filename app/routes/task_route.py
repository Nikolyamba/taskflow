from datetime import date
from typing import List

from enum import Enum as PyEnum

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.get_db import get_db
from app.models.task_model import Task
from app.models.user_model import User
from app.routes.jwt_tokens import get_current_user

task_router = APIRouter()

class TaskRegister(BaseModel):
    title: str
    description: str
    due_date: date

@task_router.post("/tasks")
async def create_task(data: TaskRegister, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    try:
        user = db.query(User).filter(User.user_name == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Вы не авторизованы!")
        new_task = Task(title = data.title,
                        description = data.description,
                        due_date = data.due_date,
                        user_id = user.id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return {"message": f"Задача {new_task.title} успешно создана", "Пользователь": f"{user.user_name}"}
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Ошибка на сервере")

class TaskStatus(PyEnum):
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"

class TaskInfo(BaseModel):
    title: str
    description: str
    status: TaskStatus
    due_date: date
    user_id: str

    class Config:
        orm_mode = True

@task_router.get("/tasks", response_model=List[TaskInfo])
async def get_user_task(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> List[TaskInfo]:
    try:
        user = db.query(User).filter(User.user_name == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Вы не авторизованы")
        tasks = db.query(Task).filter(Task.user_id == user.id).all()
        return tasks
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

class UpdateTaskStatus(BaseModel):
    status: TaskStatus

@task_router.patch("/tasks/{task_id}", response_model=TaskInfo)
async def change_task_status(task_id: str, data: UpdateTaskStatus,
                             current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> TaskInfo:
    try:
        user = db.query(User).filter(User.user_name == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Вы не авторизованы")
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена!")
        if user.id != task.user_id:
            raise HTTPException(status_code=403, detail="Вы не можете изменить статус задачи!")
        task.status = data.status
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

@task_router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    try:
        user = db.query(User).filter(User.user_name == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Вы не авторизованы")
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена!")
        if user.id != task.user_id:
            raise HTTPException(status_code=403, detail="Вы не можете удалить задачу!")
        db.delete(task)
        db.commit()
        return {"message": "Задача успешно удалена!"}
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")






