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


def profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Изменить текущий вес", callback_data="edit_current_weight")],
            [InlineKeyboardButton(text="✏️ Изменить целевой вес", callback_data="edit_goal_weight")],
            [InlineKeyboardButton(text="🎯 Изменить уровень активности", callback_data="choose_activity_level")],
            [InlineKeyboardButton(text="⚤ Изменить пол", callback_data="choose_sex")],
        ]
    )
    return kb

def sex_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Мужчина", callback_data="edit_sex:Мужчина")],
            [InlineKeyboardButton(text="Женщина", callback_data="edit_sex:Женщина")],
        ]
    )
    return kb


def activity_level_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Сидячий", callback_data="edit_activity_level:сидячий")],
            [InlineKeyboardButton(text="Обычный", callback_data="edit_activity_level:обычный")],
            [InlineKeyboardButton(text="Активный", callback_data="edit_activity_level:активный")],
        ]
    )
    return kb