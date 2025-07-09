from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.get_db import get_db
from app.models.user_model import User
from app.routes.jwt_tokens import create_access_token, create_refresh_token
import bcrypt

user_router = APIRouter()

class Register(BaseModel):
    user_name: str
    password: str

def hashed_password(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

@user_router.post("/register")
async def user_register(user: Register, db: Session = Depends(get_db)) -> dict:
    try:
        old_user = db.query(User).filter(User.user_name == user.user_name).first()
        if old_user:
            raise HTTPException(status_code=400, detail="Такой пользователь уже существует!")
        new_user = User(user_name = user.user_name,
                        password = hashed_password(user.password),
                        access_token = create_access_token(data={"sub": user.user_name}),
                        refresh_token = create_refresh_token(data={"sub": user.user_name}))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": f"Пользователь {new_user.user_name} успешно создан!", "access_token": new_user.access_token,
                "refresh_token": new_user.refresh_token}
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

@user_router.get("/users/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)) -> dict:
    try:
        current_user = db.query(User).filter(User.id == user_id).first()
        if not current_user:
            raise HTTPException(status_code=404, detail="Пользователя с таким id не существует!")
        user = User(id = current_user.id,
                    user_name = current_user.user_name,
                    password = current_user.password,
                    access_token = current_user.access_token,
                    refresh_token = current_user.refresh_token)
        return user
    except Exception as e:
        print(f"Ошибка: {e}")
        raise HTTPException(status_code=500, detail="Произошла ошибка на сервере")

