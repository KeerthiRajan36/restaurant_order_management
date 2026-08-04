from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.auth import UserRegister
from app.schemas.auth import UserLogin

from app.utils.password import (
    hash_password,
    verify_password
)

from app.utils.jwt import create_access_token

from app.exceptions.custom_exceptions import (
    AlreadyExistsException,
    UnauthorizedException
)


class AuthService:

    @staticmethod
    def register(db: Session, request: UserRegister):

        existing_user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:
            raise AlreadyExistsException(
                "Email already registered."
            )

        user = User(
            full_name=request.full_name,
            email=request.email,
            password=hash_password(request.password),
            role=request.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login(db: Session, request: UserLogin):

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if user is None:
            raise UnauthorizedException(
                "Invalid email or password."
            )

        if not verify_password(
            request.password,
            user.password
        ):
            raise UnauthorizedException(
                "Invalid email or password."
            )

        token = create_access_token(
            {
                "user_id": user.id,
                "email": user.email,
                "role": user.role.value
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }