import io
import base64
import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.utils.db_manager import DataBaseManager
from src.utils.service_manager import ServiceManager
from src.utils.states import CalorieState
from src.keyboards.inline import add_calories_kb
from src.keyboards.main_menu import main_kb

router = Router()


@router.message(CalorieState.waiting_for_calories, F.photo)
async def process_calorie_photo(
    message: Message,
    service_manager: ServiceManager,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    buffer = io.BytesIO()
    await message.bot.download(message.photo[-1], destination=buffer)
    image_bytes = buffer.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    answer_text = await service_manager.openai.analyze_image(base64_image)

    numbers = re.findall(r"\d+", answer_text)
    if numbers:
        calories = int(numbers[0])
        await state.update_data(pending_calories=calories)
        await message.answer(answer_text, reply_markup=add_calories_kb(calories))
    else:
        await message.answer(answer_text + "\n\nНе удалось определить калории. Попробуйте другое фото или введите число (ккал) вручную:")


@router.message(CalorieState.waiting_for_calories, F.text)
async def process_calorie_text(
    message: Message,
    db_manager: DataBaseManager,
    state: FSMContext,
):
    text = message.text.strip().replace(",", ".")
    try:
        calories = int(float(text))
    except ValueError:
        await message.answer("Пожалуйста, отправьте <b>фото блюда</b> или введите <b>число</b> (ккал):", parse_mode="HTML")
        return

    total = await db_manager.cache.add_daily_calories(message.from_user.id, calories)
    await state.clear()
    await message.answer(
        f"✅ Добавлено <b>{calories}</b> ккал.\n"
        f"Всего за сегодня: <b>{total}</b> ккал.",
        parse_mode="HTML",
        reply_markup=main_kb(),
    )


@router.message(CalorieState.waiting_for_calories)
async def process_calorie_invalid(
    message: Message,
):
    await message.answer("Пожалуйста, отправьте <b>фото блюда</b> или введите <b>число</b> (ккал):", parse_mode="HTML")
