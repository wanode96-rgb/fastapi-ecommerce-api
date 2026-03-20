from pydantic import BaseModel
from typing import Optional
from app.schemas.category import CategoryResponse


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_available: bool
    category_id: Optional[int] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    is_available: bool | None = None