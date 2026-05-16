from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.utils.db_manager import DataBaseManager

router = Router()


@router.callback_query(F.data.startswith("add_cal:"))
async def add_calories_callback(
    callback: CallbackQuery,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    calories = int(callback.data.split(":")[1])
    total = await db_manager.cache.add_daily_calories(callback.from_user.id, calories)
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
    total = await db_manager.cache.get_daily_calories(callback.from_user.id)
    await callback.message.edit_text(f"📊 Всего потреблено калорий сегодня: {total} ккал.")
    await callback.answer()
