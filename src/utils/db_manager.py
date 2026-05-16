from src.databases.sql import sessions

from src.repository.cache_repository import CacheRepository
from src.repository.users_repository import UsersRepository


class DataBaseManager:
    def __init__(self, session_factory=None, redis_client=None):
        self.__session_factory = session_factory
        self.__redis_client = redis_client
    #менеджер контекста
    async def __aenter__(self):
        self.session = self.__session_factory()

        self.users = UsersRepository(self.session)
        self.cache = CacheRepository(self.__redis_client)
        return self
    async def __aexit__(self, *args, **kwargs):
        if self.__redis_client:
            await self.__redis_client.aclose()
        await self.session.rollback()
        await self.session.close()
    async def commit(self):
        await self.session.commit()
