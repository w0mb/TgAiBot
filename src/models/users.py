from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseOrm


class UsersOrm(BaseOrm):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    