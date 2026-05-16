from sqlalchemy import BigInteger, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from src.databases.sql import BaseOrm


class UsersOrm(BaseOrm):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    profile_name: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    current_weight: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    goal_weight: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)