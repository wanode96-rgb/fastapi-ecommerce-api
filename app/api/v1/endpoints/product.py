from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.schemas.common import MessageResponse
from app.crud.crud_product import create_product, get_all_products, update_product, delete_product
from app.core.dependencies import get_current_admin, get_current_user
from typing import Optional

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
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(get_current_user),
):
    return await get_all_products(
        session,
        search=search, 
        min_price=min_price, 
        max_price=max_price
        )


# ✅ Update Endpoint (PUT/PATCH)
@router.put("/{product_id}", response_model=ProductResponse)
async def update_existing_product(
    product_id: int,
    product: ProductUpdate,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(get_current_admin), # Added _ and matched function name
):
    updated_product = await update_product(session, product_id, product)

    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated_product


# ✅ Delete Endpoint
# Using MessageResponse here makes your Swagger docs look professional
@router.delete("/{product_id}", response_model=MessageResponse)
async def delete_existing_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(get_current_admin), # Added _ and matched function name
):
    deleted_product = await delete_product(session, product_id)

    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}