from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


from .schemas import UserCreationSchema
from .models import User
from .utils import hash_password


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    query = select(User).where(User.email == email)
    result = await session.exec(query)
    return result.first()


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    query = select(User).where(User.username == username)
    result = await session.exec(query)
    return result.first()


async def create_account(data: UserCreationSchema, session: AsyncSession) -> User:
    dumped_data = data.model_dump()

    # Create a new user instance
    new_user = User(**dumped_data)
    new_user.password_hash = hash_password(data.password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def email_exists(email: str, session: AsyncSession) -> bool:
    user = await get_user_by_email(email, session)
    return True if user is not None else False


async def username_exists(username: str, session: AsyncSession) -> bool:
    user = await get_user_by_username(username, session)
    return True if user is not None else False
