import asyncio
from argon2 import PasswordHasher

ph = PasswordHasher()

async def hash_password_argon2(password: str) -> str:
    return await asyncio.to_thread(ph.hash, password)

async def verify_password_argon2(hash: str, password: str) -> bool:
    return await asyncio.to_thread(ph.verify, hash, password)



