from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать привычку"),
            KeyboardButton(text="Создать задачу")
        ],
        [
            KeyboardButton(text="Посмотреть текущие задачи"),
            KeyboardButton(text="Посмотреть текущие привычки")
        ],
        [
            KeyboardButton(text="Отметить задачу выполненной")
        ]
    ],
    resize_keyboard=True, input_field_placeholder="Выберите нужный вариант"
)

kb_back_or_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Вернуться в начало"),
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True, input_field_placeholder="Выберите нужный вариант"
)

kb_frequency = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="daily"),
            KeyboardButton(text="weekly"),
            KeyboardButton(text="monthly")
        ]
    ],
    resize_keyboard=True, input_field_placeholder="Выберите нужный вариант"
)