from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def daily_progress_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Дневной прогресс", callback_data="daily_progress")],
        ]
    )
    return kb


def add_calories_kb(calories: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"➕ Добавить {calories} ккал", callback_data=f"add_cal:{calories}")],
        ]
    )
    return kb
