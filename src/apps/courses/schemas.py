from typing import Optional
from pydantic import BaseModel


class CourseCreationSchema(BaseModel):
    title: str
    description: str


class CourseUpdatingSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None