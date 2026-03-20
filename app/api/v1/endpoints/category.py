from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_session
from app.core.dependencies import get_current_admin, get_current_user
from app.schemas.category import CategoryCreate, CategoryResponse
from app.crud.crud_category import create_category, get_categories

router = APIRouter(tags=["categories"])

# 🔐 Admin Only: Create a new category
@router.post("/", response_model=CategoryResponse)
async def add_category(
    category: CategoryCreate,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(get_current_admin), # Only admins can add categories
):
    return await create_category(session, category)

# 👤 Any User: List all categories
@router.get("/", response_model=List[CategoryResponse])
async def list_categories(
    session: AsyncSession = Depends(get_session),
    _: None = Depends(get_current_user),
):
    return await get_categories(session)