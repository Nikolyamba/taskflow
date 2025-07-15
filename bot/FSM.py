from aiogram.fsm.state import StatesGroup, State

class AuthStates(StatesGroup):
    waiting_for_credentials = State()