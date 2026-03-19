from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_session
from app.core.dependencies import get_current_user
from app.schemas.order import OrderResponse
from app.crud.crud_order import create_order_from_cart
from app.models.user import User

router = APIRouter(tags=["orders"])

# 💳 Checkout: Convert Cart to Order
@router.post("/checkout", response_model=OrderResponse)
async def checkout(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    order = await create_order_from_cart(session, current_user.id)
    
    if not order:
        raise HTTPException(
            status_code=400, 
            detail="Cart is empty or could not be processed"
        )
    
    return order

# 📜 Order History: View all past orders
@router.get("/history", response_model=List[OrderResponse])
async def get_order_history(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # This uses the relationship we added to the User model!
    return current_user.orders