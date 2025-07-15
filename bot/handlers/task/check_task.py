from aiogram import F, types

from app.models.task_model import Task
from app.models.user_model import User
from bot.bot_main import dp, get_tg_db
from bot.keyboards import kb_start


@dp.message(F.text == "Посмотреть задачи")
async def check_tasks(message: types.Message):
    with get_tg_db() as db:
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        tasks = db.query(Task).filter(Task.user_id == user.id).all()
        if not tasks:
            await message.answer("У тебя пока нет задач.")
            return

        task_info = []

        for task in tasks:
            task_info.append(
                f"📌 *{task.title}*\n"
                f"📝 {task.description}\n"
                f"📅 До: {task.due_date.strftime('%d.%m.%Y')}\n"
                f"✅ Статус: {task.status.value}\n"
                f"ID: {task.id}"
            )

        await message.answer("\n\n".join(task_info), parse_mode="Markdown", reply_markup=kb_start)