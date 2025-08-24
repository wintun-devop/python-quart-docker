import threading
import time
import secrets
import base64

_counter = 0
_counter_lock = threading.Lock()

def cuid() -> str:
    global _counter
    with _counter_lock:
        _counter += 1
        count = _counter
    # Timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    # Counter in hex
    count_hex = f"{count:x}"
    # Random entropy (base32, URL-safe)
    entropy = base64.b32encode(secrets.token_bytes(8)).decode("utf-8").lower().rstrip("=")
    # Format: c + timestamp + counter + entropy
    return f"c{timestamp:x}{count_hex}{entropy}"
