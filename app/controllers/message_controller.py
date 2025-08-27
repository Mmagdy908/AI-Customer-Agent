from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.message_service import MessageService
from app.config.dbconfig import get_db

router = APIRouter()


@router.get("/{thread_id}", status_code=200)
async def get_all(thread_id: str, db: Session = Depends(get_db)):
    message_service = MessageService(db)

    return {"response": message_service.get_all_messages(thread_id)}
