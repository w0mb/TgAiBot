from pydantic import BaseModel


class UsersAdd(BaseModel):
    user_id: int

class Users(UsersAdd):
    id: int
