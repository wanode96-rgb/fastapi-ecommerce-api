from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User
from app.core.db import get_session
from app.core.security import verify_password, create_access_token
from app.schemas.user import UserLogin, Token
from datetime import timedelta
from app.core.config import settings

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, session: AsyncSession = Depends(get_session)):
    # 1️⃣ Select the user from DB
    query = select(User).where(User.email == form_data.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    # 2️⃣ Check if user exists and password matches
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3️⃣ Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": "admin" if user.is_admin else "user"},
        expires_delta=access_token_expires
    )

    # 4️⃣ Return token
    return {"access_token": access_token, "token_type": "bearer"}