from pydantic import BaseModel
from datetime import datetime

class InventoryCreate(BaseModel):
    name: str
    model_no: str
    price: float = 0
    qty: int = 0

class InventoryRead(InventoryCreate):
    id: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True

class InventoryUpdate(BaseModel):
    name: str | None = None
    model_no: str | None = None
    price: float | None = None
    qty: int | None = None

