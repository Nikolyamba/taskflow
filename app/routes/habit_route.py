from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from enum import Enum as PyEnum

from sqlalchemy.orm import Session

from app.db.get_db import get_db
from app.models.habit_model import Habit
from app.models.user_model import User
from app.routes.jwt_tokens import get_current_user

habit_router = APIRouter()

class HabitFrequency(PyEnum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class HabitRegister(BaseModel):
    title: str
    description: str
    frequency: HabitFrequency
    last_done: Optional[datetime] = None

@habit_router.post("/habits")
async def create_habit(data: HabitRegister, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    try:
        user = db.query(User).filter(User.user_name == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Вы не авторизованы!")
        new_habit = Habit(title = data.title,
                          description = data.description,
                          frequency = data.frequency,
                          last_done = data.last_done,
                          user_id = user.id)
        db.add(new_habit)
        db.commit()
        db.refresh(new_habit)
        return {"message": f"Привычка {new_habit.title} успешно добавлена!"}
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

class HabitInfo(HabitRegister):
    user_id: str

    class Config:
        orm_mode = True

@habit_router.get("/habits")
async def check_habits(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> List[HabitInfo]:
    try:
        user = db.query(User).filter(User.user_name == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Вы не авторизованы")
        habits = db.query(Habit).filter(Habit.user_id == user.id).all()
        return habits
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

@habit_router.patch("/habits/{habit_id}")
async def change_last_done(habit_id: str, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> HabitInfo:
    try:
        user = db.query(User).filter(User.user_name == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Вы не авторизованы")
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit:
            raise HTTPException(status_code=404, detail="Привычка не найдена")
        if user.id != habit.user_id:
            raise HTTPException(status_code=403, detail="Вы не можете изменить привычку!")
        habit.last_done = datetime.utcnow()
        db.commit()
        db.refresh(habit)
        return habit
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

@habit_router.get("/habits/report")
async def habit_report(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    try:
        user = db.query(User).filter(User.user_name == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Вы не авторизованы")
        habits = db.query(Habit).filter(Habit.user_id == user.id).all()
        habit_info = {}
        for habit in habits:
            if habit.last_done is None:
                habit_info[habit.title] = "Привычка ещё не выполнялась"
                continue
            if habit.frequency == HabitFrequency.daily:
                if datetime.utcnow() - habit.last_done > timedelta(days=1):
                    days_lost = datetime.utcnow() - habit.last_done
                    habit_info[habit.title] = f"Вы уже не выполняли привычку: {days_lost} дней!"
            elif habit.frequency == HabitFrequency.weekly:
                if datetime.utcnow() - habit.last_done > timedelta(days=7):
                    weeks_lost = (datetime.utcnow() - habit.last_done).days // 7
                    habit_info[habit.title] = f"Вы уже не выполняли привычку: {weeks_lost} недель!"
            else:
                if datetime.utcnow() - habit.last_done > timedelta(days=30):
                    months_lost = (datetime.utcnow() - habit.last_done).days // 30
                    habit_info[habit.title] = f"Вы уже не выполняли привычку: {months_lost} месяцев!"
        return habit_info
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")