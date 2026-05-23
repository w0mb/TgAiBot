


import hashlib
from datetime import date

from redis.asyncio import Redis


class CacheRepository:
    def __init__(self, client: Redis):
        self.client = client

    def _get_image_hash(self, image_bytes: bytes) -> str:
        return hashlib.sha256(image_bytes).hexdigest()

    def _get_cache_key(self, user_id: int, image_bytes: bytes) -> str:
        image_hash = self._get_image_hash(image_bytes)
        return f"vision_cache:{user_id}:{image_hash}"

    async def get_response(self, user_id: int, image_bytes: bytes) -> str | None:
        key = self._get_cache_key(user_id, image_bytes)
        result = await self.client.get(key)
        return result.decode() if result else None

    async def set_response(self, user_id: int, image_bytes: bytes, response: str, ttl: int = 60):
        key = self._get_cache_key(user_id, image_bytes)
        await self.client.setex(key, ttl, response)

    async def get_ttl(self, user_id: int, image_bytes: bytes) -> int:
        key = self._get_cache_key(user_id, image_bytes)
        return await self.client.ttl(key)

    def _daily_key(self, user_id: int) -> str:
        return f"daily_calories:{user_id}:{date.today().isoformat()}"

    async def get_daily_calories(self, user_id: int) -> int:
        key = self._daily_key(user_id)
        val = await self.client.get(key)
        return int(val) if val else 0

    async def add_daily_calories(self, user_id: int, amount: int) -> int:
        key = self._daily_key(user_id)
        total = await self.client.incrby(key, amount)
        await self.client.expire(key, 86400)
        return total