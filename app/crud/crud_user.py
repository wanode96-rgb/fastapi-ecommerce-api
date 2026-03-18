from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate):
    # 1. Check existing user
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        return None  # handle in endpoint

    # 2. Hash password
    hashed_password = hash_password(user.password)

    # 3. Create user object
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )

    # 4. Save to DB
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user