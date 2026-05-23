from src.models.notification import NotificationOrm
from src.repository.base_repository import BaseRepository
from src.schemas.notifications import Notification


class NotificationsRepository(BaseRepository):
    model = NotificationOrm
    schema = Notification
