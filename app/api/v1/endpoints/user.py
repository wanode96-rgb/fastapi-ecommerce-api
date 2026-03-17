from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.schemas.user import UserCreate, UserRead
from app.crud.crud_user import create_user

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(session, user)