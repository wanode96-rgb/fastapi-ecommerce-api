from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import Optional, TYPE_CHECKING

# This prevents circular imports during type checking
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.product import Product

class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"

    # 1. Unique Constraint: Prevents duplicate rows for the same user + product
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="unique_user_product_cart"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(default=1, ge=1) # ge=1 ensures quantity is at least 1

    # 2. Relationships (The "Magic" part)
    # This allows you to do: cart_item.product.name
    user: "User" = Relationship(back_populates="cart_items")
    product: "Product" = Relationship()