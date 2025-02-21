import uuid

from sqlmodel import Field

from src.core.db.base_models import TimeStamped


class Course(TimeStamped, table=True):
    __tablename__ = "courses"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str

    def __repr__(self):
        return f"<Course {self.title}>"
