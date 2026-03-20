from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rating: int = Field(ge=1, le=5)  # ⬅️ CS Logic: Greater than or equal to 1, Less than or equal to 5
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 🔗 Links
    product_id: int = Field(foreign_key="product.id")
    user_id: int = Field(foreign_key="user.id")

    # 👥 Relationships
    product: "Product" = Relationship(back_populates="reviews")
    user: "User" = Relationship(back_populates="reviews")