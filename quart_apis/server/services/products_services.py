from sqlalchemy.ext.asyncio import AsyncSession
from server.models import Product



async def item_create(session: AsyncSession, data:Product) -> Product:
    item = Product(**data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item