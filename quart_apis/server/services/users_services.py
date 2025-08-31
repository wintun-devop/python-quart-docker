from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from server.models import User

async def user_create(session: AsyncSession, data:User) -> User:
    user = User(**data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def user_get_one(session:AsyncSession,id:str)->User | None:
    result = await session.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()

async def user_update(session: AsyncSession, id: str, data: dict) -> User | None:
    result = await session.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user

async def user_delete(session: AsyncSession, id: str) -> bool:
    result = await session.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if not user:
        return False
    await session.delete(user)
    await session.commit()
    return True


async def item_get_all(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()