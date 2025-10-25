### Initialize the alembic
- creates an alembic/ folder and an alembic.ini config file
```
alembic init alembic
```
- configure alembic
 - Open alembic.ini and set your database URL under the [alembic] section
```
[alembic]
script_location = alembic
sqlalchemy.url = postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME
```
### Configure env.py for AsyncEngine
- Replace the sync engine setup with an async-aware version.
```
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# import your Base metadata
from your_app.db.models import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    return config.get_main_option("sqlalchemy.url")

async def run_migrations_online():
    connectable = create_async_engine(
        get_url(),
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # detect column type changes
    )
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    import asyncio
    asyncio.run(run_migrations_online())
```
### Generate Model
```
alembic revision --autogenerate -m "initial user model"
```
### Make Migration
```
alembic upgrade head
```