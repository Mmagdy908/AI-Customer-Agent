from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.agent_service import AgentService
from app.models.prompt import Prompt
from app.config.dbconfig import get_db

router = APIRouter()


@router.get("/", status_code=200)
async def get_all(db: Session = Depends(get_db)):
    agent_service = AgentService(db)

    return {"response": agent_service.get_all_threads()}


@router.post("/", status_code=200)
async def send_prompt(prompt: Prompt, db: Session = Depends(get_db)):
    agent_service = AgentService(db)
    return {
        "response": agent_service.send_agent_prompt(prompt.content, prompt.thread_id)
    }
