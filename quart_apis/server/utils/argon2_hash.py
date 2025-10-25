import asyncio
from argon2 import PasswordHasher,exceptions as argon2_ex

ph = PasswordHasher()

async def hash_password_argon2(password: str) -> str:
    return await asyncio.to_thread(ph.hash, password)

""" async def verify_password_argon2(hash: str, password: str) -> bool:
    return await asyncio.to_thread(ph.verify, hash, password)
"""

async def verify_password_argon2(hash_str: str, password: str) -> dict:
    """
    Verify password against argon2 hash in an async-safe way.
    Returns a dict with either {"ok": True} or {"ok": False, "error": "<code>", "detail": "<message>"}.
    """
    def _verify():
        try:
            ph.verify(hash_str, password)
            # optional: check if hash needs rehashing
            needs_rehash = ph.check_needs_rehash(hash_str)
            return {"ok": True, "needs_rehash": needs_rehash}
        except argon2_ex.VerifyMismatchError:
            return {"ok": False, "error": "invalid_credentials", "detail": "password does not match"}
        except argon2_ex.InvalidHash:
            return {"ok": False, "error": "invalid_hash", "detail": "stored hash is malformed"}
        except argon2_ex.VerificationError:
            return {"ok": False, "error": "verification_failed", "detail": "verification failed"}
        except argon2_ex.Argon2Error as e:
            return {"ok": False, "error": "argon2_error", "detail": str(e)}
        except Exception as e:
            return {"ok": False, "error": "internal_error", "detail": str(e)}
    return await asyncio.to_thread(_verify)



