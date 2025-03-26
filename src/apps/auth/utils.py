import uuid
import logging
from datetime import datetime, timedelta
from typing_extensions import TypedDict
from passlib.context import CryptContext

import jwt

from src.configs.settings import JWTConfigs


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_configs = JWTConfigs()


class JWTPayload(TypedDict):
    user: str
    exp: int
    jti: uuid.UUID
    refresh: bool


def hash_password(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    exp = datetime.now() + timedelta(seconds=jwt_configs.JWT_EXPIRATION)
    if expiry:
        exp = datetime.now() + expiry

    payload: JWTPayload = {
        "user": user_data,
        "exp": exp,
        "jti": uuid.uuid4().hex,
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload,
        key=jwt_configs.JWT_SECRET,
        algorithm=jwt_configs.JWT_ALGORITHM,
    )
    return token


def decode_token(token: str) -> JWTPayload:
    try:
        return jwt.decode(
            token,
            key=jwt_configs.JWT_SECRET,
            algorithms=[jwt_configs.JWT_ALGORITHM],
        )

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
