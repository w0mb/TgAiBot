import base64
import io
import re

from aiogram import F, Router
from aiogram.types import Message

from src.keyboards.inline import add_calories_kb
from src.utils.db_manager import DataBaseManager
from src.utils.service_manager import ServiceManager


router = Router()


@router.message(F.photo)
async def handle_message(
    message: Message,
    service_manager: ServiceManager,
    db_manager: DataBaseManager,
):
    buffer = io.BytesIO()
    await message.bot.download(message.photo[-1], destination=buffer)
    image_bytes = buffer.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    try:
        cached_response = await db_manager.cache.get_response(message.from_user.id, image_bytes)
    except Exception:
        cached_response = None

    if cached_response:
        try:
            ttl = await db_manager.cache.get_ttl(message.from_user.id, image_bytes)
        except Exception:
            ttl = "?"
        await message.answer(cached_response + f"Из кеша ttl: {ttl}")
        return

    answer_text = await service_manager.openai.analyze_image(base64_image)
    try:
        await db_manager.cache.set_response(message.from_user.id, image_bytes, answer_text, ttl=60)
    except Exception:
        pass

    numbers = re.findall(r"\d+", answer_text)
    if numbers:
        calories = int(numbers[0])
        await message.answer(answer_text, reply_markup=add_calories_kb(calories))
    else:
        await message.answer(answer_text)
