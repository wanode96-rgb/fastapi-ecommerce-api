import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.core.db import engine
from app.models.product import Product, Category
from app.models.user import User
from app.core.security import hash_password

# Import these to handle the Foreign Key constraints
from app.models.review import Review
# If you have cart and order models, import them. 
# If not yet created, comment these two lines out:
from app.models.cart import CartItem 
from app.models.order import OrderItem

async def seed_data():
    async with AsyncSession(engine) as session:
        print("🌱 Starting Seed Process...")

        # 🔥 STEP 1: CLEAR OLD DATA (Order matters!)
        print("🗑️ Clearing old data to avoid Foreign Key errors...")
        try:
            # Delete children first
            await session.execute(delete(Review))
            await session.execute(delete(OrderItem))
            await session.execute(delete(CartItem))
            # Delete parent last
            await session.execute(delete(Product))
            await session.commit()
            print("✅ Old data cleared.")
        except Exception as e:
            await session.rollback()
            print(f"⚠️ Note: Some tables might not exist yet, skipping clear: {e}")

        # 1. Handle Categories safely
        category_data = [
            {"name": "Electronics", "desc": "Gadgets, phones, and laptops"},
            {"name": "Fashion", "desc": "Clothing, shoes, and accessories"},
            {"name": "Home & Kitchen", "desc": "Furniture and appliances"},
            {"name": "Books", "desc": "Fiction, Non-fiction, and Tech"},
            {"name": "Fitness", "desc": "Gym gear and health supplements"}
        ]
        
        categories = []
        for cat in category_data:
            statement = select(Category).where(Category.name == cat["name"])
            result = await session.execute(statement)
            existing_cat = result.scalar_one_or_none()
            
            if not existing_cat:
                db_cat = Category(name=cat["name"], description=cat["desc"])
                session.add(db_cat)
                categories.append(db_cat)
                print(f"Created category: {cat['name']}")
            else:
                categories.append(existing_cat)
                print(f"Category already exists: {cat['name']}")
        
        await session.commit()
        for c in categories: 
            await session.refresh(c)

        # 2. Generate 50 Products
        print("📦 Adding 50 random products...")
        prefixes = ["Ultra", "Smart", "Classic", "Premium", "Eco", "Pro", "Master"]
        items = ["Gadget", "Device", "Apparel", "Book", "Tool", "Kit", "Gear"]

        for i in range(1, 51):
            random_cat = random.choice(categories)
            price = round(random.uniform(500.0, 95000.0), 2)
            
            product = Product(
                name=f"{random.choice(prefixes)} {random.choice(items)} {i}",
                description=f"High-quality item from our {random_cat.name} collection.",
                price=price,
                is_available=True,
                category_id=random_cat.id
            )
            session.add(product)

        # 3. Handle Admin
        admin_email = "admin@example.com"
        statement = select(User).where(User.email == admin_email)
        result = await session.execute(statement)
        if not result.scalar_one_or_none():
            admin_user = User(
                email=admin_email,
                full_name="Admin Vaibhav",
                hashed_password=hash_password("admin123"),
                is_admin=True
            )
            session.add(admin_user)
            print("👤 Admin user created.")

        await session.commit()
        print(f"✅ Seeding Complete! 50 products are now live.")

if __name__ == "__main__":
    asyncio.run(seed_data())