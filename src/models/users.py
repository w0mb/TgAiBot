from enum import Enum as PyEnum
from sqlalchemy import BigInteger, Float, Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.databases.sql import BaseOrm


class ActivityLevel(str, PyEnum):
    SEDENTARY = "сидячий"
    NORMAL = "обычный"
    ACTIVE = "активный"


class UsersOrm(BaseOrm):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    profile_name: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    current_weight: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    goal_weight: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    age: Mapped[int] = mapped_column(Integer, CheckConstraint("age > 0 and age < 120"), nullable=False, default=0)
    height: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    activity_level: Mapped[str] = mapped_column(String(32), nullable=False, default=ActivityLevel.NORMAL.value)
    sex: Mapped[str] = mapped_column(String(8), nullable=False)
    @validates('age')
    def validate_age(self, key, value):
        if not 0 < value < 120:
            raise ValueError("При добавлении в базу данных пришел не корректный возраст")
        return value

    @validates('activity_level')
    def validate_activity_level(self, key, value):
        ActivityLevel(value)
        return value
    
    @validates("sex")
    def validate_sex(self, key, value):
        if value not in ("Мужчина", "Женщина"):
            raise ValueError("При добавлении в базу данных пришел не корректный пол")
        return value
