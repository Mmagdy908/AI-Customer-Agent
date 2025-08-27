from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, db: Session):
        self.mesaage_repository = MessageRepository(db)

    def get_all_messages(self, thread_id: str):
        return self.mesaage_repository.get_all_messages(thread_id)
