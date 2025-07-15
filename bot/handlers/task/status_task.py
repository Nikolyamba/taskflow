from uuid import UUID

from aiogram import F, types
from aiogram.fsm.context import FSMContext

from app.models.task_model import Task
from app.models.user_model import User
from app.routes.task_route import TaskStatus
from bot.FSM import CheckTask
from bot.bot_main import dp, get_tg_db
from bot.keyboards import kb_start


@dp.message(F.text == "Отметить задачу выполненной")
async def start_change_status(message: types.Message, state: FSMContext):
    await message.answer("Введите ID задачи\nДля того чтобы узнать id посмотрите список ваших задач")
    await state.set_state(CheckTask.waiting_task_id)

@dp.message(CheckTask.waiting_task_id)
async def change_status_tg(message: types.Message, state: FSMContext):
    with get_tg_db() as db:
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        task_id = UUID(message.text)
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            await message.answer("Задача не найдена. Убедись, что ID правильный.")
            return

        if task.user_id != user.id:
            await message.answer("Ты не можешь менять статус для этой задачи!")
            return

        task.status = TaskStatus.done
        db.commit()
        await message.answer(f"Задача '{task.title}' отмечена как выполненная ✅", parse_mode="Markdown", reply_markup=kb_start)
        await state.clear()