from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings

engine = create_async_engine(settings.postgres_url)
sessions = async_sessionmaker(bind=engine)
class BaseOrm(DeclarativeBase): ...
