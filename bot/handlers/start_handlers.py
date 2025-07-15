from contextlib import contextmanager

from aiogram.filters import CommandStart
from aiogram import types
from aiogram.fsm.context import FSMContext

from app.db.session import SessionLocal
from app.models.user_model import User
from app.routes.user_route import hashed_password
from bot.FSM import AuthStates
from bot.bot_main import dp

from bot.keyboards import kb_start

@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("Привет, пользователь)\nПрежде чем мы начнём, укажи свой user name и пароль, который ты вводил при регистрации!"
                         "\nВводить необходимо сначала user name и через пробел пароль")
    await state.set_state(AuthStates.waiting_for_credentials)

@contextmanager
def get_tg_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@dp.message(AuthStates.waiting_for_credentials)
async def get_user_name(message: types.Message, state: FSMContext):
    with get_tg_db() as db:
        try:
            user_name = message.text.split()[0]
            password = hashed_password(message.text.split()[1])
        except:
            await message.answer("Вы некорректно ввели логин и пароль")
            return

        user = db.query(User).filter((User.user_name == user_name) & (User.password == password)).first()
        if not user:
            await message.answer("Логин или пароль не верен или такого пользователя не существует")
            await state.clear()
        else:
            await message.answer(f"Привет, {user_name}!", reply_markup=kb_start)
            user.telegram_id = message.from_user.id
            db.commit()
            await state.clear()