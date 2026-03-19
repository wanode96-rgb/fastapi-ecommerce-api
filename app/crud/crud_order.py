from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.order import Order, OrderItem
from app.models.cart import CartItem

async def create_order_from_cart(db: AsyncSession, user_id: int):
    # 1. Fetch Cart Items
    result = await db.execute(
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .options(selectinload(CartItem.product))
    )
    cart_items = result.scalars().all()

    if not cart_items:
        return None

    # 2. Calculate Total
    total = sum(item.quantity * item.product.price for item in cart_items)

    # 3. Create Order
    new_order = Order(user_id=user_id, total_amount=total)
    db.add(new_order)
    await db.flush()  # Get the new_order.id

    # 4. Move items to OrderItem (Freezing the price)
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.product.price
        )
        db.add(order_item)
        await db.delete(cart_item)  # Clear the cart

    await db.commit()
    
    # 🔥 THE FIX: Re-fetch the order with all relationships loaded
    result = await db.execute(
        select(Order)
        .where(Order.id == new_order.id)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product) # Eager load both levels
        )
    )
    return result.scalar_one()