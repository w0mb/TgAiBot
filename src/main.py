import asyncio
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnectionError

from middleware.db_middleware import DataBaseMiddleWare
from middleware.service_middleware import ServiceManagerMiddleware
from src.config import settings
from src.handlers.callback_handler import router as callback_router
from src.handlers.calorie_handler import router as calorie_router
from src.handlers.image_handler import router as image_router
from src.handlers.main_menu_handler import router as main_menu_router
from src.handlers.notification_handler import router as notification_router
from src.handlers.start_handler import router as start_router
from src.databases.sql import sessions
from src.repository.notifications_repository import NotificationsRepository
from src.services.notification import notification_service
from src.utils.bot_provider import BotProvider
from src.utils.proxy_parser import get_valid_proxies

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
dp = Dispatcher()
image_router.message.middleware(ServiceManagerMiddleware())
calorie_router.message.middleware(ServiceManagerMiddleware())
dp.update.middleware(DataBaseMiddleWare())

dp.include_routers(
    start_router,
    image_router,
    main_menu_router,
    callback_router,
    calorie_router,
    notification_router,
)


async def main():
    urls = await asyncio.to_thread(get_valid_proxies)
    bot = None

    while True:
        for url in urls:
            try:
                session = AiohttpSession(proxy=url, timeout=120.0)
                bot = Bot(token=settings.bot_token, session=session)
                await bot.get_me()
                logging.info(f"Подключились через прокси {url}")
                BotProvider.set_bot(bot)
                try:
                    notification_service.scheduler.start()
                    async with sessions() as session:
                        repo = NotificationsRepository(session)
                        notifs = await repo.get_all()
                        notification_service.load_all(notifs)
                except Exception:
                    logger.exception("Не удалось запустить планировщик уведомлений")
                break
            except Exception as e:
                logging.warning(f"Прокси {url} не работает: {e}")
        else:
            logging.error("Нет рабочих прокси, жду 30с и обновляю список...")
            urls = await asyncio.to_thread(get_valid_proxies)
            await asyncio.sleep(30)
            continue

        try:
            await dp.start_polling(bot, polling_timeout=20)
        except (ProxyConnectionError, OSError, Exception) as e:
            logging.error(f"Соединение потеряно через прокси {url}: {e}")
            if bot:
                await bot.session.close()
            urls = await asyncio.to_thread(get_valid_proxies)
            continue


if __name__ == "__main__":
    asyncio.run(main())
