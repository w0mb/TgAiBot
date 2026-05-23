from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
            [InlineKeyboardButton(text="✏️ Изменить рост", callback_data="edit_height")],
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


def notification_list_kb(notifications: list) -> InlineKeyboardMarkup:
    rows = []
    for n in notifications:
        status = "✅" if n.enable else "⬜"
        rows.append([
            InlineKeyboardButton(text=f"{status} {n.time}", callback_data=f"notif_toggle:{n.id}"),
            InlineKeyboardButton(text="❌", callback_data=f"notif_delete:{n.id}"),
        ])
    rows.append([InlineKeyboardButton(text="➕ Добавить", callback_data="notif_add")])
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


def notification_time_kb() -> InlineKeyboardMarkup:
    times = [f"{h:02d}:00" for h in range(8, 23)]
    rows = []
    for i in range(0, len(times), 3):
        row = [InlineKeyboardButton(text=t, callback_data=f"notif_time:{t}") for t in times[i:i+3]]
        rows.append(row)
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb
