from sqlmodel import SQLModel, Field
from typing import Optional


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    is_available: bool = True