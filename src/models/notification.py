from sqlalchemy import BigInteger, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.databases.sql import BaseOrm


class NotificationOrm(BaseOrm):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    enable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    time: Mapped[str] = mapped_column(String(5), nullable=False, default="20:00")
