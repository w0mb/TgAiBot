from aiogram import BaseMiddleware
from aiogram.types import Message

from src.utils.service_manager import ServiceManager


class ServiceManagerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        if isinstance(event, Message) and event.photo:
            async with ServiceManager() as service_manager:
                data["service_manager"] = service_manager
                return await handler(event, data)
        return await handler(event, data)
