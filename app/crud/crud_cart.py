from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload # 🔥 Add this
from app.models.cart import CartItem

# ➕ Add to cart (Upsert Logic)
async def add_to_cart(db: AsyncSession, user_id: int, product_id: int, quantity: int):
    # Search for existing item in THIS user's cart
    result = await db.execute(
        select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        ).options(selectinload(CartItem.product))
    )
    cart_item = result.scalar_one_or_none()

    if cart_item:
        cart_item.quantity += quantity # Update
    else:
        cart_item = CartItem( # Insert
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)
        # For a brand new item, we need to load the product before returning
        await db.flush() # Send to DB but don't commit yet
        # Refresh to trigger the selectinload for the new object
        result = await db.execute(
            select(CartItem)
            .where(CartItem.id == cart_item.id)
            .options(selectinload(CartItem.product))
        )
        cart_item = result.scalar_one()

    await db.commit()
    return cart_item

# 📦 Get user cart (With Eager Loading)
async def get_cart(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .options(selectinload(CartItem.product)) # 🔥 Fetches product details in 1 query
    )
    return result.scalars().all()

# ❌ Remove item (Secure Delete)
async def remove_from_cart(db: AsyncSession, cart_id: int, user_id: int):
    result = await db.execute(
        select(CartItem).where(
            CartItem.id == cart_id,
            CartItem.user_id == user_id # Ensures user owns the cart item
        )
    )
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        return None

    await db.delete(cart_item)
    await db.commit()
    return cart_item