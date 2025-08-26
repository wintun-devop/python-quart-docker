from sqlalchemy.ext.asyncio import AsyncSession
from server.models import Inventory
from sqlalchemy import select



async def item_create(session: AsyncSession, data:Inventory) -> Inventory:
    item = Inventory(**data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

async def item_get_one(session:AsyncSession,id:str)->Inventory | None:
    result = await session.execute(select(Inventory).where(Inventory.id == id))
    return result.scalar_one_or_none()

async def item_update(session: AsyncSession, id: str, data: dict) -> Inventory | None:
    result = await session.execute(select(Inventory).where(Inventory.id == id))
    item = result.scalar_one_or_none()
    if not item:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item

async def item_delete(session: AsyncSession, id: str) -> bool:
    result = await session.execute(select(Inventory).where(Inventory.id == id))
    item = result.scalar_one_or_none()
    if not item:
        return False
    await session.delete(item)
    await session.commit()
    return True

async def item_get_all(session: AsyncSession) -> list[Inventory]:
    result = await session.execute(select(Inventory))
    return result.scalars().all()

