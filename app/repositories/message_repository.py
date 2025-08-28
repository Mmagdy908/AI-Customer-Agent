from app.models.message import Message
from sqlalchemy.orm import Session
import copy


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, thread_id: str, role: str, content: str):
        new_message = Message(thread_id=thread_id, role=role, content=content)
        self.db.add(new_message)
        self.db.commit()
        self.db.refresh(new_message)
        return copy.deepcopy(new_message)

    # get all messages of a thread
    def get_all_messages(self, thread_id: str):
        messages = (
            self.db.query(Message)
            .filter(Message.thread_id == thread_id)
            .order_by(Message.created_at.desc())
            .all()
        )

        return list(map(lambda m: {"id":m.id,"role": m.role, "content": m.content,"created_at": m.created_at}, messages))
