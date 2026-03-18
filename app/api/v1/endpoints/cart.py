from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_session
from app.core.dependencies import get_current_user
from app.schemas.cart import CartAdd, CartResponse
from app.crud.crud_cart import add_to_cart, get_cart, remove_from_cart
from app.models.user import User

router = APIRouter(tags=["cart"])

# ➕ Add to cart
@router.post("/", response_model=CartResponse)
async def add_item_to_cart(
    item: CartAdd,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # This now returns the newly created/updated item
    cart_item = await add_to_cart(session, current_user.id, item.product_id, item.quantity)
    
    # We manually calculate total_price for the response
    return {
        **cart_item.__dict__,
        "product": cart_item.product,
        "total_price": cart_item.quantity * cart_item.product.price
    }

# 📦 View cart
@router.get("/", response_model=List[CartResponse])
async def view_cart(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    items = await get_cart(session, current_user.id)
    
    # Format the list to include the calculated total_price
    return [
        {
            **item.__dict__,
            "product": item.product,
            "total_price": item.quantity * item.product.price
        }
        for item in items
    ]

# ❌ Remove item
@router.delete("/{cart_id}")
async def remove_item(
    cart_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    deleted = await remove_from_cart(session, cart_id, current_user.id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Cart item not found")

    return {"message": "Item removed from cart"}