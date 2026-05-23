from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.keyboards.inline import profile_kb
from src.utils.calorie_calculator import calculate_daily_norm
from src.utils.db_manager import DataBaseManager
from src.utils.states import CalorieState


router = Router()

@router.message(F.text == "📖 Обо мне")
async def handle_about(message: Message):
    await message.answer("Ковалев Даниил ИП-217, бот-помошник по контролю питания")

@router.message(F.text == "👤 Профиль")
async def handle_user_profile(
    message: Message,
    db_manager: DataBaseManager,
):
    user = await db_manager.users.get_filtred(user_id=message.from_user.id)
    if user is None:
        await message.answer("Профиль не найден. Введите /start для регистрации.")
        return

    daily_norm = calculate_daily_norm(user.current_weight, user.goal_weight, user.age, user.height, user.activity_level, user.sex)
    try:
        calories_today = await db_manager.cache.get_daily_calories(message.from_user.id)
    except Exception:
        calories_today = "—"
    goal_direction = "похудение" if user.goal_weight < user.current_weight else "набор массы" if user.goal_weight > user.current_weight else "поддержание веса"
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

@router.message(F.text == "🍽️ Добавить калории")
async def handle_add_calories(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    try:
        total = await db_manager.cache.get_daily_calories(message.from_user.id)
    except Exception:
        total = "—"
    await state.set_state(CalorieState.waiting_for_calories)
    await message.answer(
        f"🍽️ Всего потреблено калорий сегодня: <b>{total}</b> ккал.\n\n"
        f"Отправьте <b>фото блюда</b> для определения калорий или введите <b>число</b> (ккал) вручную:",
        parse_mode="HTML",
    )
