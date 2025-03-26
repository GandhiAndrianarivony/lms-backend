from datetime import timedelta
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
)

from src.core.db.async_database import get_session_db

from ..models import User
from ..schemas import UserCreationSchema, UserLoginSchema
from .. import services as AccountService
from .. import utils as auth_utils


REFRESH_TOKEN_EXPIRE_DAYS = 2

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


@auth_router.post("/login")
async def login(
    response: Response, data: UserLoginSchema, session=Depends(get_session_db)
):
    dumped_data = data.model_dump()

    if dumped_data.get("username") is not None:
        user = await AccountService.get_user_by_username(
            dumped_data["username"], session=session
        )

    else:
        user = await AccountService.get_user_by_email(
            dumped_data["email"], session=session
        )

    # User should have an account before log in
    if user is not None:
        is_valid_password = auth_utils.verify_password(
            dumped_data["password"], user.password_hash
        )
        if is_valid_password:
            access_token = auth_utils.create_access_token(
                user_data={
                    "email": dumped_data.get("email", ""),
                    "username": dumped_data.get("username", ""),
                    "user_id": str(user.id),
                }
            )
            refresh_token = auth_utils.create_access_token(
                user_data={
                    "email": dumped_data.get("email", ""),
                    "username": dumped_data.get("username", ""),
                    "user_id": str(user.id),
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
                refresh=True,
            )

            response.set_cookie(
                key="access_token", value=f"Bearer {access_token}", httponly=True
            )
            response.set_cookie(
                key="refresh_token",
                value=f"Bearer {refresh_token}",
                httponly=True,
                samesite="Lax",
                # secure=True,
            )
            return {"message": "Login successful"}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@auth_router.get("/logout")
async def logout(request: Response):
    request.delete_cookie("access_token")
    request.delete_cookie("refresh_token")
    return {"message": "Logout successful"}
