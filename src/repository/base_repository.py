from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from src.schemas.users import Users
from src.database import BaseOrm

class BaseRepository:
    session: AsyncSession
    model: BaseOrm
    schema: BaseModel
    def __init__(self, session):
        self.session = session
    async def add(self, data: Users) -> None:
        try:
            stmt = insert(self.model).values(**data.model_dump())
            await self.session.execute(stmt)
        except:
            raise Exception("Ошибка при добавлении в базу данных")
        await self.session.commit()
    async def get_one(self) -> BaseModel:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return self.schema.model_validate(result.scalars().one())
    async def get_all(self) -> list[BaseModel]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return [self.schema.model_validate(obj) for obj in result.scalars().all()]