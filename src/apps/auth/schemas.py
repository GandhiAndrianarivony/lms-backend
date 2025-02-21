from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserCreationSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(min_length=8)
    email: EmailStr = Field(max_length=100)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
