import redis.asyncio

from src.config import settings

connection_pool = redis.asyncio.ConnectionPool.from_url(settings.redis_url)


def get_redis_client() -> redis.asyncio.Redis:
    return redis.asyncio.Redis(connection_pool=connection_pool)