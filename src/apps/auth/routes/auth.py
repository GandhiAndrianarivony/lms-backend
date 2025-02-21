from fastapi import APIRouter, Depends, HTTPException, status

from src.core.db.async_database import get_session_db

from ..models import User
from ..schemas import UserCreationSchema
from .. import services as AccountService


auth_router = APIRouter(tags=["Authentication"], prefix="/auth")


@auth_router.post(
    "/signup",
    response_model=User,
)
async def create_account(data: UserCreationSchema, session=Depends(get_session_db)):
    email_exists = await AccountService.email_exists(data.email, session)
    username_exists = await AccountService.username_exists(data.username, session)

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with `{data.email}` already exists",
        )
    elif username_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with `{data.username}` already exists",
        )

    user = await AccountService.create_account(data, session)
    return user
