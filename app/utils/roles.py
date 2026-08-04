from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.utils.jwt import verify_access_token

security = HTTPBearer()


def get_current_user(
    credential: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credential.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    user = db.query(User).filter(
        User.id == payload["user_id"]
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def require_roles(*roles):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):

        if current_user.role.value not in roles:

            raise HTTPException(
                status_code=403,
                detail="Permission Denied"
            )

        return current_user

    return role_checker