from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession  # ⬅️ Fixes "AsyncSession"
from typing import List

# Internal Imports
from app.core.db import get_session
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse  # ⬅️ Fixes "ReviewCreate/Response"
from app.crud.crud_review import create_review  # ⬅️ Fixes "create_review"

router = APIRouter(tags=["reviews"])

@router.post("/{product_id}/", response_model=ReviewResponse)
async def post_review(
    product_id: int,
    review_in: ReviewCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Optional: Logic to check if product exists before reviewing
    return await create_review(
        db=db, 
        review_data=review_in, 
        user_id=current_user.id, 
        product_id=product_id
    )