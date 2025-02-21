import uuid
from typing import List

from fastapi import APIRouter, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.async_database import get_session_db

from ..models import Course
from ..schemas import CourseCreationSchema, CourseUpdatingSchema
from .. import services as CourseService


course_router = APIRouter(tags=["Courses"], prefix="/courses")


@course_router.get("/", response_model=List[Course])
async def get_courses(
    database_session: AsyncSession = Depends(get_session_db),
) -> List[Course]:
    """
    Get a list of all the courses.
    """
    return await CourseService.list(database_session)


@course_router.post("/create")
async def create_course(
    course: CourseCreationSchema,
    database_session: AsyncSession = Depends(get_session_db),
) -> Course:
    book = await CourseService.create(course, database_session)
    return book


@course_router.delete("/delete/{id}")
async def delete_course(
    id: uuid.UUID, database_session: AsyncSession = Depends(get_session_db)
) -> Response:
    await CourseService.delete(id=id, session=database_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@course_router.get("/detail/{id}")
async def get_course(
    id: uuid.UUID, database_session: AsyncSession = Depends(get_session_db)
) -> Course:
    return await CourseService.get(id=id, session=database_session)


@course_router.patch("/update/{id}")
async def update_course(
    id: uuid.UUID,
    course: CourseUpdatingSchema,
    database_session: AsyncSession = Depends(get_session_db),
) -> Course:
    return await CourseService.update(data=course, id=id, session=database_session)
