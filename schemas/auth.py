from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    email: EmailStr


class UserSignUp(User):
    password: str = Field(min_length=8)


class UserInDB(User):
    model_config = ConfigDict(from_attributes=True)

    hashed_password: str


class UserRead(User):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
