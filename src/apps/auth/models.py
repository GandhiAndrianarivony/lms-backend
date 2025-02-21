import uuid

from pydantic import EmailStr
from sqlmodel import Field

from src.core.db.base_models import TimeStamped


class User(TimeStamped, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    password_hash: str = Field(exclude=True)
    is_verified: bool = Field(default=False)

    def __repr__(self):
        return f"<User {self.username}>"
