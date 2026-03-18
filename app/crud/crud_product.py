from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product
from app.schemas.product import ProductCreate


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