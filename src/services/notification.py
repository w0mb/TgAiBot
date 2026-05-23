import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.utils.bot_provider import BotProvider

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.scheduler = self._create_scheduler()

    @staticmethod
    def _create_scheduler():
        try:
            import redis
            from apscheduler.jobstores.redis import RedisJobStore
            from src.config import settings
            r = redis.Redis(host=settings.redis_host, port=int(settings.redis_port))
            r.ping()
            r.close()
            logger.info("Redis доступен, используется RedisJobStore")
            return AsyncIOScheduler(jobstores={
                "default": RedisJobStore(host=settings.redis_host, port=int(settings.redis_port)),
            })
        except Exception:
            logger.warning("Redis недоступен, планировщик работает без сохранения задач")
            return AsyncIOScheduler()

    async def send_notification(self, user_id: int) -> None:
        try:
            bot = BotProvider.get_bot()
            await bot.send_message(
                chat_id=user_id,
                text="🔔 Напоминание! Не забудьте записать свои калории за сегодня. Введите число или отправьте фото блюда.",
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления: {e}")

    def schedule_notification(self, notif_id: int, user_id: int, time_str: str) -> None:
        try:
            hour, minute = map(int, time_str.split(":"))
            self.scheduler.add_job(
                self.send_notification,
                "cron",
                hour=hour,
                minute=minute,
                args=[user_id],
                id=f"notification_{notif_id}",
                replace_existing=True,
                misfire_grace_time=300,
            )
        except Exception as e:
            logger.error("Ошибка планирования уведомления: %s", e)

    def remove_notification(self, notif_id: int) -> None:
        job_id = f"notification_{notif_id}"
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)

    def load_all(self, notifications: list) -> None:
        for n in notifications:
            if n.enable:
                self.schedule_notification(n.id, n.user_id, n.time)


notification_service = NotificationService()
