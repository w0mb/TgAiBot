from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

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

    calories_today = await db_manager.cache.get_daily_calories(message.from_user.id)
    text = (
        f"<b>👤 Профиль</b>\n\n"
        f"<b>Имя:</b> {user.profile_name}\n"
        f"<b>Текущий вес:</b> {user.current_weight} кг\n"
        f"<b>Целевой вес:</b> {user.goal_weight} кг\n"
        f"<b>Калории за сегодня:</b> {calories_today} ккал\n"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "🍽️ Добавить калории")
async def handle_add_calories(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    total = await db_manager.cache.get_daily_calories(message.from_user.id)
    await state.set_state(CalorieState.waiting_for_calories)
    await message.answer(
        f"🍽️ Всего потреблено калорий сегодня: <b>{total}</b> ккал.\n\n"
        f"Отправьте <b>фото блюда</b> для определения калорий или введите <b>число</b> (ккал) вручную:",
        parse_mode="HTML",
    )