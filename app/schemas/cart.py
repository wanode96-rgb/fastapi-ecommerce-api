from pydantic import BaseModel, Field, computed_field
from typing import List
from app.schemas.product import ProductResponse # Reuse your existing schema!

class CartAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)

class CartResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    # Magic Link: This nests the product details inside the cart item
    product: ProductResponse 

    # The "Magic" Computed Field
    @computed_field
    @property
    def subtotal(self) -> float:
        # CS Logic: price * quantity
        return round(self.product.price * self.quantity, 2)

    class Config:
        from_attributes = True


    class CartListResponse(BaseModel):
        items: List[CartResponse]
        
        @computed_field
        @property
        def total_price(self) -> float:
            return sum(item.subtotal for item in self.items)