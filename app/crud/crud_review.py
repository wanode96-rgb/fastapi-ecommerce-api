from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review import Review
from app.schemas.review import ReviewCreate

async def create_review(db: AsyncSession, review_data: ReviewCreate, user_id: int, product_id: int):
    # Combine the user input with the IDs from the system
    db_review = Review(
        **review_data.model_dump(),
        user_id=user_id,
        product_id=product_id
    )
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review