from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.dbconfig import get_db
from app.models.user import (
    UserDTO,
    UserCreateRequest,
    UserWithToken,
    UserCredentials,
)
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/register", response_model=UserDTO, status_code=201)
async def register(user: UserCreateRequest, db: Session = Depends(get_db)) -> UserDTO:
    """
    Create a new user.
    """
    auth_service = AuthService(db)
    return auth_service.register(user)


@router.post("/login", response_model=UserWithToken)
async def login(user: UserCredentials, db: Session = Depends(get_db)) -> UserWithToken:
    """Authenticate a user and return an access token."""
    auth_service = AuthService(db)
    return auth_service.login(user)
