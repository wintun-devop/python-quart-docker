### alembic initialization
```
alembic init migrations
```

### alembic db-source configuration-postgresql
- Alembic needs a sync engine to run migrations
```
[app]
sqlalchemy.url = postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:{port}/${DB_NAME}
```

### import model to env.py as Admin setup config env.py
```
from __init__ import Base
target_metadata = Base.metadata
```

### migration
```
alembic revision --autogenerate -m "your migration name"
```
```
alembic upgrade heads
```