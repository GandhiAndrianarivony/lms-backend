from typing import Optional
from pydantic import BaseModel, Field, EmailStr, model_validator


class UserCreationSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(min_length=8)
    email: EmailStr = Field(max_length=100)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @model_validator(mode="after")
    def format_name(self):
        self.username = self.username.strip().title()
        self.first_name = self.first_name.strip().title() if self.first_name else None
        return self


class UserLoginSchema(BaseModel):
    username: str | None = Field(max_length=50, default=None)
    email: EmailStr | None = Field(max_length=100, default=None)
    password: str = Field(min_length=8)

    @model_validator(mode="after")
    def check_username_or_email(self):
        if not self.username and not self.email:
            raise ValueError("Username or email is required")
        return self
