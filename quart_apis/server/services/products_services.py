from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from server.models import Inventory



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

#upsert base on id
async def item_upsert(session: AsyncSession, data: dict) -> Inventory:
    stmt = insert(Inventory).values(**data)
    # Define conflict target and update logic
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],  
        set_={key: value for key, value in data.items() if key != "id"}
    )
    await session.execute(stmt)
    await session.commit()
    # Optionally fetch the updated row
    result = await session.execute(
        select(Inventory).where(Inventory.id == data["id"])
    )
    return result.scalar_one()


async def item_upsert_many(session: AsyncSession, data: list[dict]) -> list[dict]:
    results = []
    # ensures transactional integrity
    async with session.begin():  
        for item in data:
            stmt = insert(Inventory).values(**item)
            stmt = stmt.on_conflict_do_update(
                index_elements=["model"],  # adjust to your unique constraint
                set_={key: value for key, value in item.items() if key != "model"}
            )
            result = await session.execute(stmt)
            results.append(result.scalar_one())
    return results

