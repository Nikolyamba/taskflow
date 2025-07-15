from aiogram.fsm.state import StatesGroup, State

class AuthStates(StatesGroup):
    waiting_for_credentials = State()

class CreateTask(StatesGroup):
    title = State()
    description = State()
    due_date = State()

class CreateHabit(StatesGroup):
    title = State()
    description = State()
    frequency = State()

class CheckTask(StatesGroup):
    waiting_task_id = State()

class SetLastDone(StatesGroup):
    waiting_habit_id = State()