from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.cart import CartItem  # Prevents circular import loop

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False

    cart_items: List["CartItem"] = Relationship(back_populates="user")