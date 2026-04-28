from src.repository.users_repository import UsersRepository


class DataBaseManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
    #менеджер контекста
    async def __aenter__(self):
        self.session = self.__session_factory()
        self.users = UsersRepository(self.session)
        return self
    async def __aexit__(self, *args, **kwargs):
        await self.session.rollback()
        await self.session.close()
    async def commit(self):
        await self.session.commit()
