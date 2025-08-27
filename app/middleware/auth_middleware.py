from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.config.dbconfig import get_db
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import jwt
import os
from app.models.user import UserInDb


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")),
    db: Session = Depends(get_db),
) -> UserInDb:
    """
    Dependency to get the current user from the token.
    """

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )

    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user
