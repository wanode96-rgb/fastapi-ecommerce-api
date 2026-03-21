from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from sqlalchemy import or_
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from app.models.review import Review


async def create_product(db: AsyncSession, product: ProductCreate):
    # it safely converts your schema into a dictionary for SQLMode
    db_product = Product(**product.model_dump())

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)

    return db_product


async def get_all_products(
        db: AsyncSession,
        search: str = None, 
        min_price: float = None, 
        max_price: float = None,
        category_id: int = None,
        skip: int = 0,
        limit: int = 10
        ):
    query = select(Product).options(selectinload(Product.category))

    count_query = select(func.count()).select_from(Product)

    filters = []
    if search:
        filters.append(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )

    if min_price is not None:
        filters.append(Product.price >= min_price)
        
    if max_price is not None:
         filters.append(Product.price <= max_price)
    
    if category_id:
        filters.append(Product.category_id == category_id)

    if filters:
        for f in filters:
            query = query.where(f)
            count_query = count_query.where(f)

    # 4. Execute Count
    total_result = await db.execute(count_query)
    total_count = total_result.scalar()

    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    products = result.scalars().all()
    return products, total_count


async def get_product_with_stats(db: AsyncSession, product_id: int):
    # 1. Fetch the Product
    product_query = select(Product).where(Product.id == product_id).options(selectinload(Product.category))
    product_result = await db.execute(product_query)
    product = product_result.scalar_one_or_none()

    if not product:
        return None

    # 2. 🔥 Calculate Stats from the Review table
    stats_query = select(
        func.avg(Review.rating).label("average"),
        func.count(Review.id).label("count")
    ).where(Review.product_id == product_id)
    
    stats_result = await db.execute(stats_query)
    stats = stats_result.one() # Returns a tuple (average, count)

    # 3. Create a dictionary to merge the data
    # This prevents the "object has no attribute" error we had earlier
    product_data = product.model_dump()
    
    # Manually add the category back if it exists (since model_dump might miss relationship objects)
    product_data["category"] = product.category 
    
    # Inject the fresh stats
    product_data["average_rating"] = round(stats.average, 1) if stats.average else 0.0
    product_data["review_count"] = stats.count

    return product_data # Return the dict; FastAPI will validate it against ProductResponse


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