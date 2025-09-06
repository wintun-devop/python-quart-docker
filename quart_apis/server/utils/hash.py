# import asyncio
# from server import bcrypt
import bcrypt



# async def hash_password(password: str) -> str:
#     # salt = bcrypt.gensalt(rounds=10)
#     hashed = await asyncio.to_thread(bcrypt.generate_password_hash, password)
#     return hashed.decode("utf-8")

# async def check_password(password: str, hashed: str) -> bool:
#     return await asyncio.to_thread(bcrypt.check_password_hash, hashed, password)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)  # You can lower rounds for speed
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
