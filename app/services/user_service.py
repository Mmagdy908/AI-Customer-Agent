from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def get_user_by_id(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)
