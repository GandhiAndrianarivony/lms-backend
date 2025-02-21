from typing import List
import uuid

from fastapi import HTTPException, status

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from .schemas import CourseCreationSchema, CourseUpdatingSchema
from .models import Course


async def _get_course_by_id(id: uuid.UUID, session: AsyncSession) -> Course:
    statement = select(Course).where(Course.id == id)
    result = await session.exec(statement)
    course = result.one()
    return course


async def list(session: AsyncSession) -> List[Course]:
    statement = select(Course).order_by(desc(Course.created_at))
    result = await session.exec(statement)
    return result.all()


async def create(data: CourseCreationSchema, session: AsyncSession) -> Course:
    dumped_data = data.model_dump()
    new_course = Course(**dumped_data)
    session.add(new_course)
    await session.commit()
    return new_course


async def delete(id: uuid.UUID, session: AsyncSession):
    try:
        course = await _get_course_by_id(id=id, session=session)
        await session.delete(course)
        await session.commit()

    except MultipleResultsFound as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multiple result where found",
        )

    except NoResultFound as _:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No result where found"
        )


async def update(data: CourseUpdatingSchema, id: uuid.UUID, session: AsyncSession):
    try:
        course = await _get_course_by_id(id=id, session=session)

        new_course_data = data.model_dump(exclude_unset=True)
        old_course_data = course.model_dump()

        updated_course_data = {**old_course_data, **new_course_data}
        print(f"[INFO] updated_course_data\n: {updated_course_data}")

        for key, value in updated_course_data.items():
            setattr(course, key, value)

        await session.commit()
        await session.refresh(course)
        return course

    except MultipleResultsFound as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multiple result where found",
        )

    except NoResultFound as _:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No result where found"
        )


async def get(id: uuid.UUID, session: AsyncSession):
    try:
        return await _get_course_by_id(id=id, session=session)

    except MultipleResultsFound as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multiple result where found",
        )

    except NoResultFound as _:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No result where found"
        )
