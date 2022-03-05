from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    is_active: bool


class CreateUserSchema(UserBase):
    pass


class UpdateUserSchema(UserBase):
    pass
