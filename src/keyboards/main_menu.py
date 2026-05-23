from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb() -> None:
    kb_list = [
        [KeyboardButton(text="📖 Обо мне"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="🍽️ Добавить калории")],
        [KeyboardButton(text="🔔 Уведомления")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
    return keyboard