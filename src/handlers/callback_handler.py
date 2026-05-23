from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards.inline import activity_level_kb, profile_kb, sex_kb
from src.schemas.users import UsersUpdate
from src.utils.calorie_calculator import calculate_daily_norm
from src.utils.db_manager import DataBaseManager
from src.utils.states import EditWeightState

router = Router()


@router.callback_query(F.data == "choose_activity_level")
async def choose_activity_level_callback(
    callback: CallbackQuery,
):
    await callback.message.edit_text("Выберите уровень активности:", reply_markup=activity_level_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("edit_activity_level"))
async def edit_activity_level_callback(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    activity_level = callback.data.split(":")[1]
    await db_manager.users.update(UsersUpdate(activity_level=activity_level), user_id=callback.from_user.id)

    user = await db_manager.users.get_filtred(user_id=callback.from_user.id)
    daily_norm = calculate_daily_norm(user.current_weight, user.goal_weight, user.age, user.height, user.activity_level, user.sex)
    goal_direction = "похудение" if user.goal_weight < user.current_weight else "набор массы" if user.goal_weight > user.current_weight else "поддержание веса"
    try:
        calories_today = await db_manager.cache.get_daily_calories(callback.from_user.id)
    except Exception:
        calories_today = "—"
    text = (
        f"<b>👤 Профиль</b>\n\n"
        f"<b>Имя:</b> {user.profile_name}\n"
        f"<b>Пол:</b> {user.sex}\n"
        f"<b>Текущий вес:</b> {user.current_weight} кг\n"
        f"<b>Целевой вес:</b> {user.goal_weight} кг\n"
        f"<b>Возраст:</b> {user.age}\n"
        f"<b>Рост:</b> {user.height} см\n"
        f"<b>Уровень активности:</b> {user.activity_level}\n"
        f"<b>Цель:</b> {goal_direction}\n"
        f"<b>Дневная норма:</b> {daily_norm} ккал\n"
        f"<b>Калории за сегодня:</b> {calories_today} ккал\n"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=profile_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("add_cal:"))
async def add_calories_callback(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    calories = int(callback.data.split(":")[1])
    try:
        total = await db_manager.cache.add_daily_calories(callback.from_user.id, calories)
    except Exception:
        await callback.message.edit_text("❌ Не удалось сохранить калории. Сервис отслеживания временно недоступен.")
        await callback.answer()
        return
    await state.clear()
    await callback.message.edit_text(
        f"✅ Добавлено {calories} ккал.\nВсего за сегодня: {total} ккал."
    )
    await callback.answer()


@router.callback_query(F.data == "daily_progress")
async def daily_progress_callback(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
):
    try:
        total = await db_manager.cache.get_daily_calories(callback.from_user.id)
    except Exception:
        total = "—"
    await callback.message.edit_text(f"📊 Всего потреблено калорий сегодня: {total} ккал.")
    await callback.answer()


@router.callback_query(F.data == "edit_current_weight")
async def edit_current_weight_callback(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(EditWeightState.waiting_for_current_weight)
    await state.update_data(profile_message_id=callback.message.message_id)
    await callback.message.edit_text("Введите новый текущий вес (кг):")
    await callback.answer()


@router.callback_query(F.data == "edit_goal_weight")
async def edit_goal_weight_callback(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(EditWeightState.waiting_for_goal_weight)
    await state.update_data(profile_message_id=callback.message.message_id)
    await callback.message.edit_text("Введите новый целевой вес (кг):")
    await callback.answer()


@router.callback_query(F.data == "edit_height")
async def edit_height_callback(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(EditWeightState.waiting_for_height)
    await state.update_data(profile_message_id=callback.message.message_id)
    await callback.message.edit_text("Введите новый рост (см):")
    await callback.answer()


@router.message(EditWeightState.waiting_for_current_weight, F.text)
async def process_new_current_weight(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    try:
        weight = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 75.5):")
        return

    await db_manager.users.update(UsersUpdate(current_weight=weight), user_id=message.from_user.id)

    data = await state.get_data()
    profile_message_id = data.get("profile_message_id")

    if profile_message_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=profile_message_id)
    await message.delete()

    user = await db_manager.users.get_filtred(user_id=message.from_user.id)
    daily_norm = calculate_daily_norm(user.current_weight, user.goal_weight, user.age, user.height, user.activity_level, user.sex)
    goal_direction = "похудение" if user.goal_weight < user.current_weight else "набор массы" if user.goal_weight > user.current_weight else "поддержание веса"
    try:
        calories_today = await db_manager.cache.get_daily_calories(message.from_user.id)
    except Exception:
        calories_today = "—"
    text = (
        f"<b>👤 Профиль</b>\n\n"
        f"<b>Имя:</b> {user.profile_name}\n"
        f"<b>Пол:</b> {user.sex}\n"
        f"<b>Текущий вес:</b> {user.current_weight} кг\n"
        f"<b>Целевой вес:</b> {user.goal_weight} кг\n"
        f"<b>Возраст:</b> {user.age}\n"
        f"<b>Рост:</b> {user.height} см\n"
        f"<b>Уровень активности:</b> {user.activity_level}\n"
        f"<b>Цель:</b> {goal_direction}\n"
        f"<b>Дневная норма:</b> {daily_norm} ккал\n"
        f"<b>Калории за сегодня:</b> {calories_today} ккал\n"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=profile_kb())
    await state.clear()


@router.message(EditWeightState.waiting_for_goal_weight, F.text)
async def process_new_goal_weight(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    try:
        weight = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer("Пожалуйста, введите число (например: 70.0):")
        return

    await db_manager.users.update(UsersUpdate(goal_weight=weight), user_id=message.from_user.id)

    data = await state.get_data()
    profile_message_id = data.get("profile_message_id")

    if profile_message_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=profile_message_id)
    await message.delete()

    user = await db_manager.users.get_filtred(user_id=message.from_user.id)
    daily_norm = calculate_daily_norm(user.current_weight, user.goal_weight, user.age, user.height, user.activity_level, user.sex)
    goal_direction = "похудение" if user.goal_weight < user.current_weight else "набор массы" if user.goal_weight > user.current_weight else "поддержание веса"
    try:
        calories_today = await db_manager.cache.get_daily_calories(message.from_user.id)
    except Exception:
        calories_today = "—"
    text = (
        f"<b>👤 Профиль</b>\n\n"
        f"<b>Имя:</b> {user.profile_name}\n"
        f"<b>Пол:</b> {user.sex}\n"
        f"<b>Текущий вес:</b> {user.current_weight} кг\n"
        f"<b>Целевой вес:</b> {user.goal_weight} кг\n"
        f"<b>Возраст:</b> {user.age}\n"
        f"<b>Рост:</b> {user.height} см\n"
        f"<b>Уровень активности:</b> {user.activity_level}\n"
        f"<b>Цель:</b> {goal_direction}\n"
        f"<b>Дневная норма:</b> {daily_norm} ккал\n"
        f"<b>Калории за сегодня:</b> {calories_today} ккал\n"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=profile_kb())
    await state.clear()


@router.message(EditWeightState.waiting_for_height, F.text)
async def process_new_height(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    try:
        height = int(message.text.strip())
        if not (50 <= height <= 250):
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите целое число от 50 до 250:")
        return

    await db_manager.users.update(UsersUpdate(height=height), user_id=message.from_user.id)

    data = await state.get_data()
    profile_message_id = data.get("profile_message_id")

    if profile_message_id:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=profile_message_id)
    await message.delete()

    user = await db_manager.users.get_filtred(user_id=message.from_user.id)
    daily_norm = calculate_daily_norm(user.current_weight, user.goal_weight, user.age, user.height, user.activity_level, user.sex)
    goal_direction = "похудение" if user.goal_weight < user.current_weight else "набор массы" if user.goal_weight > user.current_weight else "поддержание веса"
    try:
        calories_today = await db_manager.cache.get_daily_calories(message.from_user.id)
    except Exception:
        calories_today = "—"
    text = (
        f"<b>👤 Профиль</b>\n\n"
        f"<b>Имя:</b> {user.profile_name}\n"
        f"<b>Пол:</b> {user.sex}\n"
        f"<b>Текущий вес:</b> {user.current_weight} кг\n"
        f"<b>Целевой вес:</b> {user.goal_weight} кг\n"
        f"<b>Возраст:</b> {user.age}\n"
        f"<b>Рост:</b> {user.height} см\n"
        f"<b>Уровень активности:</b> {user.activity_level}\n"
        f"<b>Цель:</b> {goal_direction}\n"
        f"<b>Дневная норма:</b> {daily_norm} ккал\n"
        f"<b>Калории за сегодня:</b> {calories_today} ккал\n"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=profile_kb())
    await state.clear()
