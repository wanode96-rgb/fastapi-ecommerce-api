from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.product import ProductResponse

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    product: ProductResponse

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True