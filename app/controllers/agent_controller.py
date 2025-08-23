from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.agent_service import send_agent_prompt
from app.models.prompt import Prompt
from app.config.dbconfig import get_db

router = APIRouter()


@router.post("/", status_code=200)
async def send_prompt(prompt: Prompt, db: Session = Depends(get_db)):
    return {"response": send_agent_prompt(db, prompt.content, prompt.thread_id)}
