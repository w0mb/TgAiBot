from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select, update
from src.schemas.users import Users
from databases.sql import BaseOrm

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
    async def update(self, data: BaseModel, exclude_unset=True, **filters) -> None:
        stmt = update(self.model).filter_by(**filters).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, **filters):
        stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(stmt)
        await self.session.commit()

    async def edit(self, filters: dict, values: dict) -> BaseModel | None:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        for key, value in values.items():
            setattr(obj, key, value)
        await self.session.commit()
        return self.schema.model_validate(obj)
    async def get_filtred(self, **filters) -> BaseModel:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        return self.schema.model_validate(obj)
    async def get_one(self) -> BaseModel:
        return self.get_filtred()
    async def get_all(self) -> list[BaseModel]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return [self.schema.model_validate(obj) for obj in result.scalars().all()]