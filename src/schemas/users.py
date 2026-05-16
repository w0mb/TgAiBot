from pydantic import BaseModel, ConfigDict


class UsersAdd(BaseModel):
    user_id: int
    profile_name: str = ""
    current_weight: float = 0.0
    goal_weight: float = 0.0

class Users(UsersAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)