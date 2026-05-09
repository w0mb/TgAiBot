


import hashlib

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
    async def get_key_value(self, user_id: int, image_bytes: bytes) -> int:
        key = self._get_cache_key(user_id, image_bytes)
        value = await self.client.get(key)
        return (key, value)