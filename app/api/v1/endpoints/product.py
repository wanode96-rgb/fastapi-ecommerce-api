from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas.product import ProductCreate, ProductResponse
from app.crud.crud_product import create_product, get_all_products
from app.core.dependencies import get_current_admin, get_current_user

router = APIRouter(tags=["products"])


# 🔐 Admin only
@router.post("/", response_model=ProductResponse)
async def create_new_product(
    product: ProductCreate,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(get_current_admin),
):
    return await create_product(session, product)


# 👤 Any logged-in user
@router.get("/", response_model=list[ProductResponse])
async def list_products(
    session: AsyncSession = Depends(get_session),
    _: None = Depends(get_current_user),
):
    return await get_all_products(session)