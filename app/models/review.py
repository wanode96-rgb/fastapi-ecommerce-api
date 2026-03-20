from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rating: int = Field(ge=1, le=5)
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 🔗 Links
    product_id: int = Field(foreign_key="products.id")
    user_id: int = Field(foreign_key="users.id")

    # 👥 Relationships
    product: "Product" = Relationship(back_populates="reviews")
    user: "User" = Relationship(back_populates="reviews")