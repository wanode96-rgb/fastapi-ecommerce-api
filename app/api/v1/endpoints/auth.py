from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.core.db import get_session
from app.core.security import verify_password, create_access_token
from app.schemas.user import LoginRequest  # <-- import schema

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)):
    # 1. Query user by email
    query = select(User).where(User.email == request.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    # 2. Check credentials
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 3. Create JWT token
    access_token = create_access_token({"sub": user.email})

    # 4. Return token
    return {"access_token": access_token, "token_type": "bearer"}