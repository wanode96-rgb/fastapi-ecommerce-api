from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.cart import CartItem # Prevents circular import
    from app.models.order import OrderItem
    from app.models.review import Review

class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    is_available: bool = True

    # Add these as Optional fields
    # We don't use Field() here because we don't want them to be DB columns
    average_rating: Optional[float] = None 
    review_count: Optional[int] = None

    # This allows you to check: "Which carts contain this product?"
    cart_items: List["CartItem"] = Relationship(back_populates="product")
    order_items: List["OrderItem"] = Relationship(back_populates="product")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="products")
    reviews: List["Review"] = Relationship(back_populates="product")
    

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    
    # Relationship: One Category -> Many Products
    products: List["Product"] = Relationship(back_populates="category")