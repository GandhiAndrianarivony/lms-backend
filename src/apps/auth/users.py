from enum import Enum

from fastapi import Request, HTTPException, status

from .models import User


class UserRole(str, Enum):
    ADMIN = "admin"
    BASIC = "basic"


async def current_user(request: Request, user: User | None = None):
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")

    if not (refresh_token or access_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

