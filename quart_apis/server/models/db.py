
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from server.server_config import db_name,db_user,db_password,db_host_write,db_host_read

db_write_link = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host_write}/{db_name}"
db_read_link = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host_read}/{db_name}"

write_engine = create_async_engine(db_write_link, echo=True)
WriteSessionLocal = async_sessionmaker(write_engine, expire_on_commit=False)

read_engine = create_async_engine(db_read_link, echo=True)
ReadSessionLocal = async_sessionmaker(read_engine, expire_on_commit=False)


# Write session
async def get_write_session():
    async with WriteSessionLocal() as session:
        yield session

# Read session
async def get_read_session():
    async with ReadSessionLocal() as session:
        yield session
