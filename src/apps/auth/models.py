import uuid
from sqlmodel import Field

from src.core.db.base_models import TimeStamped


class User(TimeStamped, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)

    def __repr__(self):
        return f"<User {self.username}>"
