import logging

from sqlalchemy import insert

from src.models.users import UsersOrm
from src.repository.base_repository import BaseRepository
from src.schemas.users import Users

logger = logging.getLogger()

class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = Users

    async def add(self, data: Users) -> None:
        try:
            stmt = insert(self.model).values(**data.model_dump())
            await self.session.execute(stmt)
        except Exception as e:
            logger.critical(f"Исключение {e} скорее всего пользователь уже есть в базе данных")
        await self.session.commit()