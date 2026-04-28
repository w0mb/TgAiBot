from aiogram import BaseMiddleware

from src.utils.db_manager import DataBaseManager
from src.database import sessions

class DataBaseMiddleWare(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with DataBaseManager(sessions) as db_manager:
            data["db_manager"] = db_manager
            return await handler(event, data)