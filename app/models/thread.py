from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.config.dbconfig import Base


class Thread(Base):
    __tablename__ = "threads"

    thread_id = Column(String, primary_key=True, index=True)
    title = Column(
        String,
    )
    user_id = Column(Integer, index=True)
    # messages = Column(JSONB, default=list)
