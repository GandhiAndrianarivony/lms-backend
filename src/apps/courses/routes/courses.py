import uuid
from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

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


@course_router.post("/create", response_model=Course)
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
    try:
        await CourseService.delete(id=id, session=database_session)

    except MultipleResultsFound as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multiple result where found",
        )

    except NoResultFound as _:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No result where found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@course_router.get("/detail/{id}", response_model=Course)
async def get_course(
    id: uuid.UUID, database_session: AsyncSession = Depends(get_session_db)
) -> Course:
    try:
        return await CourseService.get(id=id, session=database_session)
    except MultipleResultsFound as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multiple result where found",
        )

    except NoResultFound as _:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No result where found"
        )


@course_router.patch("/update/{id}", response_model=Course)
async def update_course(
    id: uuid.UUID,
    course: CourseUpdatingSchema,
    database_session: AsyncSession = Depends(get_session_db),
) -> Course:
    try:
        return await CourseService.update(data=course, id=id, session=database_session)

    except MultipleResultsFound as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multiple result where found",
        )

    except NoResultFound as _:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No result where found"
        )
