from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.config.dbconfig import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, ForeignKey("threads.thread_id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship
    thread = relationship(
        "Thread",
    )
