from aiogram import F, types

from app.models.habit_model import Habit
from app.models.user_model import User
from bot.bot_main import dp, get_tg_db
from bot.keyboards import kb_start


@dp.message(F.text == "Посмотреть задачи")
async def check_habits(message: types.Message):
    with get_tg_db() as db:
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        habits = db.query(Habit).filter(Habit.user_id == user.id).all()
        if not habits:
            await message.answer("У тебя пока нет привычек.")
            return

        habit_info = []

        for habit in habits:
            habit_info.append(
                f"📌 *{habit.title}*\n"
                f"📝 {habit.description}\n"
                f"📅 Частота: {habit.frequency}\n"
                f"✅ Последнее время выполнения: {habit.last_done}\n"
                f"ID: {habit.id}"
            )

        await message.answer("\n\n".join(habit_info), parse_mode="Markdown", reply_markup=kb_start)