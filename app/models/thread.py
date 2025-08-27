from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.dbconfig import Base


class Thread(Base):
    __tablename__ = "threads"

    thread_id = Column(String, primary_key=True, index=True)
    title = Column(
        String,
    )
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    # Relationship
    user = relationship("User")
