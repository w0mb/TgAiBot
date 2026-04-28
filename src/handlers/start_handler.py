from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.utils.db_manager import DataBaseManager
from src.schemas.users import UsersAdd

router = Router()

@router.message(Command(commands=["start"]))
async def start_handler(message: Message, db_manager: DataBaseManager, **kwargs):
    await db_manager.users.add(UsersAdd(user_id=message.from_user.id))
    await message.answer("Вы добавлены в базу можете пользоваться ботом, пришлите картинку для определения калорий")