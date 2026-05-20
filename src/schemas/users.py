from pydantic import BaseModel, ConfigDict


class UsersAdd(BaseModel):
    user_id: int
    profile_name: str = ""
    current_weight: float = 0.0
    goal_weight: float = 0.0
    age: int = 0
    height: int = 0
    activity_level: str = "обычный"
    sex: str = ""


class UsersUpdate(BaseModel):
    profile_name: str | None = None
    current_weight: float | None = None
    goal_weight: float | None = None
    age: int | None = None
    height: int | None = None
    activity_level: str | None = None
    sex: str | None = None
    
class Users(UsersAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)