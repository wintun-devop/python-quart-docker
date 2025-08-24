from pydantic import BaseModel
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    model_no: str
    price: float = 0
    qty: int = 0

class ProductRead(ProductCreate):
    id: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True