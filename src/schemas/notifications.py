from pydantic import BaseModel, ConfigDict


class NotificationAdd(BaseModel):
    user_id: int
    time: str = "20:00"
    enable: bool = True


class NotificationUpdate(BaseModel):
    time: str | None = None
    enable: bool | None = None


class Notification(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    enable: bool
    time: str
