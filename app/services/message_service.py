from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.message_repository import MessageRepository
from app.repositories.thread_repository import ThreadRepository


class MessageService:
    def __init__(self, db: Session):
        self.mesaage_repository = MessageRepository(db)
        self.thread_repository = ThreadRepository(db)

    def get_all_messages(self, thread_id: str, user_id: int):
        thread = self.thread_repository.get_thread_by_id(thread_id)
        if not thread:
            raise HTTPException(404, "This thread is not found")

        if thread.user_id != user_id:
            raise HTTPException(403, "You can not access this thread")

        return self.mesaage_repository.get_all_messages(thread_id)
