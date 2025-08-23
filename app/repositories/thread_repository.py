from sqlalchemy import select
from app.models.thread import Thread
from sqlalchemy.orm import sessionmaker, Session
import copy


class ThreadRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_thread(self, thread_id: str, thread_title: str):
        new_thread = Thread(thread_id=thread_id, title=thread_title)
        self.db.add(new_thread)
        self.db.commit()
        self.db.refresh(new_thread)
        return copy.deepcopy(new_thread)

    # TODO
    # get all threads of a user
    def get_all_threads(self, user_id):
        return self.db.query(Thread).filter(Thread.user_id == user_id).all()

    def get_thread_by_id(self, thread_id: str) -> Thread | None:
        return copy.deepcopy(self.db.query(Thread).get(thread_id))

    def add_messages(self, thread_id: str, messages: list[dict[str, str]]):
        thread = self.db.query(Thread).filter(Thread.thread_id == thread_id).first()
        thread.messages = thread.messages + messages
        self.db.commit()
        self.db.refresh(thread)
        return copy.deepcopy(thread)
