from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token
)

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    request: UserRegister,
    db: Session = Depends(get_db)
):
    return AuthService.register(db, request)


@router.post(
    "/login",
    response_model=Token
)
def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):
    return AuthService.login(db, request)