from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from databases.sql import BaseOrm
from src.schemas.users import Users

class BaseRepository:
    session: AsyncSession
    model: BaseOrm
    schema: BaseModel
    def __init__(self, session):
        self.session = session
    async def add(self, data: Users):
        try:
            stmt = insert(self.model).values(**data.model_dump()).returning(*self.model.__table__.columns)
            result = await self.session.execute(stmt)
            row = result.fetchone()
        except:
            raise Exception("Ошибка при добавлении в базу данных")
        await self.session.commit()
        return self.schema.model_validate(row)
    async def update(self, data: BaseModel, exclude_unset=True, **filters) -> None:
        stmt = update(self.model).filter_by(**filters).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, **filters):
        stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_filtred(self, **filters) -> BaseModel:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        return self.schema.model_validate(obj)
    async def get_all(self, **filters) -> list[BaseModel]:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return [self.schema.model_validate(obj) for obj in result.scalars().all()]