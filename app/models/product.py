from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.cart import CartItem # Prevents circular import

class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    is_available: bool = True

    # This allows you to check: "Which carts contain this product?"
    cart_items: List["CartItem"] = Relationship(back_populates="product")