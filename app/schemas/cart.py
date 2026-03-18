from pydantic import BaseModel
from app.schemas.product import ProductResponse # Reuse your existing schema!

class CartAdd(BaseModel):
    product_id: int
    quantity: int = 1

class CartResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    # Magic Link: This nests the product details inside the cart item
    product: ProductResponse 

    class Config:
        from_attributes = True