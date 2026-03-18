from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


async def create_product(db: AsyncSession, product: ProductCreate):
    # it safely converts your schema into a dictionary for SQLMode
    db_product = Product(**product.model_dump())

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)

    return db_product


async def get_all_products(db: AsyncSession):
    # This fetches every row from the 'products' table asynchronously
    result = await db.execute(select(Product))
    return result.scalars().all()


async def update_product(db: AsyncSession, product_id: int, product_data: ProductUpdate):
    # 1. Find the product
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalar_one_or_none()

    if not db_product:
        return None

    # 2. Extract only the fields provided in the request (Pydantic v2 style)
    update_data = product_data.model_dump(exclude_unset=True)

    # 3. Apply updates dynamically
    for key, value in update_data.items():
        setattr(db_product, key, value)

    # 4. Save and Refresh
    await db.commit()
    await db.refresh(db_product)

    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalar_one_or_none()

    if not db_product:
        return None

    # Option A: Hard Delete (Learning version)
    await db.delete(db_product)
    
    # Option B: Soft Delete (Professional version)
    # db_product.is_available = False 

    await db.commit()
    # No need to refresh after a delete, but good for a soft-delete update
    if db_product.is_available == False:
        await db.refresh(db_product)

    return db_product