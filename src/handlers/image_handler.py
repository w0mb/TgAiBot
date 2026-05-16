import io
import base64
import re
from aiogram import Router
from aiogram.types import Message
from aiogram import F
from src.utils.service_manager import ServiceManager
from src.utils.db_manager import DataBaseManager
from src.keyboards.inline import add_calories_kb


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

    cached_response = await db_manager.cache.get_response(message.from_user.id, image_bytes)
    if cached_response:
        ttl = await db_manager.cache.get_ttl(message.from_user.id, image_bytes)
        await message.answer(cached_response + f"Из кеша ttl: {ttl}")
        return

    answer_text = await service_manager.openai.analyze_image(base64_image)
    await db_manager.cache.set_response(message.from_user.id, image_bytes, answer_text, ttl=60)

    numbers = re.findall(r"\d+", answer_text)
    if numbers:
        calories = int(numbers[0])
        await message.answer(answer_text, reply_markup=add_calories_kb(calories))
    else:
        await message.answer(answer_text)
