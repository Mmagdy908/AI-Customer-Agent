from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, Integer, String
from app.config.dbconfig import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class UserDTO(BaseModel):
    id: int
    full_name: str
    email: EmailStr


class UserInDb(UserDTO):
    password: str = Field(..., description="Hashed password of the user")


class UserWithToken(UserDTO):
    token: str = Field(..., description="JWT access token for the user")


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class UserCreateRequest(UserCredentials):
    full_name: str
