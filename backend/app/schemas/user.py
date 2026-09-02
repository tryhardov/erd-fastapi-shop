from pydantic import ConfigDict, Field, BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., max_length=20)
    email: EmailStr = Field(..., max_length=255)
    bio : str | None = None


class UserCreate(UserBase):
    password: str = Field(...,min_length=8, max_length=255)


class UserUpdate(BaseModel):
    username: str | None = Field(None, max_length=20)
    email: EmailStr | None = Field(None, max_length=255)
    password: str | None = Field(None,min_length=8, max_length=255)
    bio: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)