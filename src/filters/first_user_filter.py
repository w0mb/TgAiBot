from aiogram.types import Message
from aiogram.filters import BaseFilter

from src.utils.db_manager import DataBaseManager
from src.databases.sql import sessions

class IsFirstLaunch(BaseFilter):
    def __init__(self, *args, **kwargs):
        super().__init__()

    async def __call__(self, message: Message):
        async with DataBaseManager(sessions) as db:
            user = await db.users.get_filtred(user_id=message.from_user.id)
        if user:
            return False
        else:
            return True
