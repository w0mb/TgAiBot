from aiogram import BaseMiddleware

from src.utils.service_manager import ServiceManager


class ServiceManagerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with ServiceManager() as service_manager:
            data["service_manager"] = service_manager
            return await handler(event, data)
