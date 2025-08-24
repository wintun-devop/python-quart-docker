import os
from dotenv import load_dotenv

#to get to ensure from .env
load_dotenv(override=True)

# server secret(app secret) key and jwt secret key
APP_SECRET_KEY=os.getenv("APP_SECRET_KEY")
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")


# getting data from env
db_name=os.getenv("DB_NAME")
db_user=os.getenv("DB_USER")
db_password=os.getenv("DB_PASSWORD")
db_host_write=os.getenv("DB_HOST_WRITE")
db_host_read=os.getenv("DB_HOST_READ")

#API Base Path
api_base_path=os.getenv("API_BASE_PATH")


# DATABASE_LINK=f"postgresql://db_user:db_password@db_host/db_name"
# DATABASE_LINK=f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"