import asyncio
from server import bcrypt


async def hash_password(password: str) -> str:
    hashed = await asyncio.to_thread(bcrypt.generate_password_hash, password)
    return hashed.decode("utf-8")

async def check_password(password: str, hashed: str) -> bool:
    return await asyncio.to_thread(bcrypt.check_password_hash, hashed, password)
