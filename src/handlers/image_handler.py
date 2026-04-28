import io
import base64
from aiogram import Router
from aiogram.types import Message
from aiogram import F
from src.utils.service_manager import ServiceManager

buffer = io.BytesIO()

router = Router()


@router.message(F.photo)
async def handle_message(message: Message, service_manager: ServiceManager, **kwargs):
    await message.bot.download(message.photo[-1], destination=buffer)
    image_bytes = buffer.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    answer_text = await service_manager.openai.analyze_image(base64_image)
    await message.answer(answer_text)
