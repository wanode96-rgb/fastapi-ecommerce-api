from pydantic import BaseModel
from typing import Optional, List
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
    average_rating: Optional[float] = 0.0
    review_count: int = 0
    
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    is_available: bool | None = None

class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total_count: int
    page: int
    size: int