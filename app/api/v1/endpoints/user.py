from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_session
from app.schemas.user import UserCreate, UserResponse
from app.crud.crud_user import create_user
from app.core.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.common import MessageResponse

router = APIRouter(tags=["users"])


@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    new_user = await create_user(session, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return new_user


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/admin", response_model=MessageResponse)
async def admin_only(current_user: User = Depends(get_current_admin)):
    """
    Only accessible by users where is_admin is True.
    """
    return {"message": f"Welcome Admin, {current_user.full_name}"}