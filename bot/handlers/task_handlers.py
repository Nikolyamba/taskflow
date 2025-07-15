from datetime import datetime

from aiogram import types
from aiogram import F
from aiogram.fsm.context import FSMContext

from app.models.task_model import Task
from app.models.user_model import User
from bot.FSM import CreateTask
from bot.bot_main import dp, get_tg_db
from bot.keyboards import kb_back_or_cancel as kb_boc, kb_start

@dp.message(F.text == "Создать задачу")
async def start_task_creation(message: types.Message, state: FSMContext):
    await message.answer("Введи название задачи:", reply_markup=kb_boc)
    await state.set_state(CreateTask.title)

@dp.message(CreateTask.title)
async def get_title(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await message.answer("Вы в самом начале, нельзя вернуться назад!")
        return
    if message.text.lower() == "отмена":
        await message.answer("Создание задачи отменено", reply_markup=kb_start)
        await state.clear()
        return

    await state.update_data(title=message.text)
    await message.answer("Теперь введи описание:", reply_markup=kb_boc)
    await state.set_state(CreateTask.description)

@dp.message(CreateTask.description)
async def get_description(message: types.Message, state: FSMContext):
    if message.text.lower().capitalize() == "Назад":
        await message.answer("Введи название задачи:", reply_markup=kb_boc)
        await state.set_state(CreateTask.title)
        return
    if message.text.lower().capitalize() == "Отмена":
        await message.answer("Создание задачи отменено", reply_markup=kb_start)
        await state.clear()
        return

    await state.update_data(description=message.text)
    await message.answer("Теперь введи дату окончания задачи:\n"
                         "ВНИМАНИЕ! Ты должен ввести дату в формате 'ММ:ДД:ГГ'!", reply_markup=kb_boc)
    await state.set_state(CreateTask.due_date)

@dp.message(CreateTask.due_date)
async def get_due_date(message: types.Message, state: FSMContext):
    if message.text.lower().capitalize() == "Назад":
        await message.answer("Введи описание задачи:", reply_markup=kb_boc)
        await state.set_state(CreateTask.description)
        return
    if message.text.lower().capitalize() == "Отмена":
        await message.answer("Создание задачи отменено", reply_markup=kb_start)
        await state.clear()
        return

    try:
        due_date = datetime.strptime(message.text, "%m:%d:%y").date()
    except ValueError:
        await message.answer("Неверный формат даты. Введи в формате 'ММ:ДД:ГГ'")
        return

    await state.update_data(due_date=due_date)
    data = await state.get_data()

    with get_tg_db() as db:
        user_tg_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_tg_id).first()
        new_task = Task(title = data.get('title'),
                        description = data.get('description'),
                        due_date = data.get('due_date'),
                        user_id = user.id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        await message.answer(f"Задача {new_task.title} успешно создана!", reply_markup=kb_start)
        await state.clear()


