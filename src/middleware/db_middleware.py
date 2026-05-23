from aiogram import BaseMiddleware

from databases.redis import get_redis_client
from databases.sql import sessions
from src.utils.db_manager import DataBaseManager

class DataBaseMiddleWare(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with DataBaseManager(sessions, get_redis_client()) as db_manager:
            data["db_manager"] = db_manager
            return await handler(event, data)