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