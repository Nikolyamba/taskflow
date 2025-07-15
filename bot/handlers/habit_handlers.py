from aiogram import F, types
from aiogram.fsm.context import FSMContext

from app.models.habit_model import Habit
from app.models.user_model import User
from app.routes.habit_route import HabitFrequency
from bot.FSM import CreateHabit
from bot.bot_main import dp, get_tg_db
from bot.keyboards import kb_back_or_cancel as kb_boc, kb_start, kb_frequency


@dp.message(F.text == "Создать привычку")
async def start_habit_creation(message: types.Message, state: FSMContext):
    await message.answer("Введи название привычки", reply_markup = kb_boc)
    await state.set_state(CreateHabit.title)

@dp.message(CreateHabit.title)
async def get_habit_title(message: types.Message, state: FSMContext):
    if message.text.lower().capitalize() == "Назад":
        await message.answer("Вы в самом начале, вернуться назад нельзя!")
        return
    if message.text.lower().capitalize() == "Отмена":
        await message.answer("Создание привычки отменено", reply_markup=kb_start)
        await state.clear()
        return

    await state.update_data(title=message.text)
    await message.answer("Теперь введи описание привычки:", reply_markup=kb_boc)
    await state.set_state(CreateHabit.description)

@dp.message(CreateHabit.description)
async def get_habit_description(message: types.Message, state: FSMContext):
    if message.text.lower().capitalize() == "Назад":
        await message.answer("Введите название привычки:", reply_markup=kb_boc)
        await state.set_state(CreateHabit.title)
        return
    if message.text.lower().capitalize() == "Отмена":
        await message.answer("Создание привычки отменено", reply_markup=kb_start)
        await state.clear()
        return

    await state.update_data(description=message.text)
    await message.answer("Теперь укажи регулярность повторения привычки:\n"
                         "Примечание, вы также можете написать Отмена или Назад в чате", reply_markup=kb_frequency)
    await state.set_state(CreateHabit.frequency)

@dp.message(CreateHabit.frequency)
async def get_habit_frequency(message: types.Message, state: FSMContext):
    if message.text.lower().capitalize() == "Назад":
        await message.answer("Введите описание привычки:", reply_markup=kb_boc)
        await state.set_state(CreateHabit.description)
        return
    if message.text.lower().capitalize() == "Отмена":
        await message.answer("Создание привычки отменено", reply_markup=kb_start)
        await state.clear()
        return

    freq_text = message.text.lower()
    try:
        frequency = HabitFrequency(freq_text)
    except ValueError:
        await message.answer("Неверный выбор. Используй кнопки: daily, weekly, monthly", reply_markup=kb_frequency)
        return

    await state.update_data(frequency=frequency)
    data = await state.get_data()

    with get_tg_db() as db:
        user_tg_id = message.from_user.id
        user = db.query(User).filter(User.telegram_id == user_tg_id).first()

        new_habit = Habit(title = data.get('title'),
                          description = data.get('description'),
                          frequency = data.get('frequency'),
                          user_id = user.id)
        db.add(new_habit)
        db.commit()
        db.refresh(new_habit)

        await message.answer(f"Привычка '{new_habit.title}' успешно создана!", reply_markup=kb_start)
        await state.clear()






