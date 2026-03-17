from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.models.user import User
from app.core.security import verify_password
from app.core.auth import create_access_token
from app.schemas.user import UserLogin, Token

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    query = select(User).where(User.email == user.email)
    result = await session.execute(query)
    db_user = result.scalar_one_or_none()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": db_user.email, "id": db_user.id, "is_admin": db_user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}