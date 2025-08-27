from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from dotenv import load_dotenv
import os
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app.models.user import (
    UserDTO,
    UserCreateRequest,
    UserInDb,
    UserWithToken,
    UserCredentials,
)
from app.repositories.user_repository import UserRepository

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def _hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _generate_access_token(self, user: UserDTO) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode = {"user_id": user.id, "exp": expire}

        if not SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in environment variables")

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def register(self, user: UserCreateRequest):
        # Check if user already exists
        if self.user_repository.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password
        hashed_password = self._hash_password(user.password)

        # save user in db
        saved_user = self.user_repository.create_user(
            full_name=user.full_name, email=user.email, password=hashed_password
        )

        # Create User object
        new_user = UserInDb(
            id=saved_user.id,
            email=saved_user.email,
            full_name=saved_user.full_name,
            password=saved_user.password,
        )

        return new_user

    def login(self, user: UserCredentials) -> UserWithToken:
        existing_user = self.user_repository.get_user_by_email(user.email)

        if not existing_user or not self._verify_password(
            plain_password=user.password, hashed_password=existing_user.password
        ):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        # Generate access token
        token = self._generate_access_token(existing_user)
        return {**existing_user.__dict__, "token": token}
