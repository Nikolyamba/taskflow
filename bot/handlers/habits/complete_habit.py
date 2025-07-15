from datetime import datetime
from uuid import UUID

from aiogram import F, types
from aiogram.fsm.context import FSMContext

from app.models.habit_model import Habit
from app.models.user_model import User
from bot.FSM import SetLastDone
from bot.bot_main import dp, get_tg_db
from bot.keyboards import kb_start

@dp.message(F.text == "Отметить привычку выполненной")
async def start_change_last_done(message: types.Message, state: FSMContext):
    await message.answer("Введите ID привычки\nДля того чтобы узнать id посмотрите список ваших привычек")
    await state.set_state(SetLastDone.waiting_habit_id)

@dp.message(SetLastDone.waiting_habit_id)
async def set_last_done(message: types.Message, state: FSMContext):
    with get_tg_db() as db:
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        habit_id = UUID(message.text)
        habit = db.query(Habit).filter(Habit.id == habit_id).first()

        if not habit:
            await message.answer("Привычка не найдена. Убедись, что ID правильный.")
            return

        if habit.user_id != user.id:
            await message.answer("Ты не можешь указать привычку выполненной!")
            return

        habit.last_done = datetime.utcnow()

        db.commit()
        await message.answer(f"Привычка *{habit.title}* отмечена как выполненная ✅", parse_mode="Markdown", reply_markup=kb_start)
        await state.clear()
