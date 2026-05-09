import sys
from pathlib import Path



sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from contextlib import asynccontextmanager

from middleware.db_middleware import DataBaseMiddleWare
from middleware.service_middleware import ServiceManagerMiddleware
from src.config import settings
from src.utils.proxy_parser import download_proxies, read_proxies_from_file

from src.handlers.start_handler import router as start_router
from src.handlers.image_handler import router as image_router

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app):
    await asyncio.to_thread(download_proxies)
    yield
    
urls = read_proxies_from_file()
session = AiohttpSession(proxy=urls[0], timeout=120.0)
bot = Bot(token=settings.bot_token, session=session)

dp = Dispatcher()
image_router.message.middleware(ServiceManagerMiddleware())
dp.update.middleware(DataBaseMiddleWare())

dp.include_routers(start_router, image_router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
