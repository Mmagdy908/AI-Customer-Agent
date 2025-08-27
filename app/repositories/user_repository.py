from app.models.user import User
from sqlalchemy.orm import Session
import copy


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, full_name: str, email: str, password: str):
        new_user = User(full_name=full_name, email=email, password=password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return copy.deepcopy(new_user)

    def get_user_by_id(self, user_id: str) -> User | None:
        return copy.deepcopy(self.db.query(User).get(user_id))

    def get_user_by_email(self, email: str) -> User | None:
        return copy.deepcopy(self.db.query(User).filter(User.email == email).first())
