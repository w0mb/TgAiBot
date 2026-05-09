from aiogram import BaseMiddleware

from src.utils.db_manager import DataBaseManager
from databases.sql import sessions
from databases.redis import get_redis_client

class DataBaseMiddleWare(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with DataBaseManager(sessions, get_redis_client()) as db_manager:
            data["db_manager"] = db_manager
            return await handler(event, data)