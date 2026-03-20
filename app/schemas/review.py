from pydantic import BaseModel, Field
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str

class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str
    user_id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True