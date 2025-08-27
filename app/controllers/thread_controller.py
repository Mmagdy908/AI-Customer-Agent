from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.thread_service import AgentService
from app.models.prompt import Prompt
from app.models.user import UserInDb
from app.config.dbconfig import get_db
from app.middleware.auth_middleware import get_current_user

router = APIRouter()


@router.get("/", status_code=200)
async def get_all(
    db: Session = Depends(get_db), current_user: UserInDb = Depends(get_current_user)
):
    agent_service = AgentService(db)

    return {"response": agent_service.get_all_threads(current_user.id)}


@router.post("/send_prompt", status_code=200)
async def send_prompt(prompt: Prompt, db: Session = Depends(get_db)):
    agent_service = AgentService(db)
    return {
        "response": agent_service.send_agent_prompt(prompt.content, prompt.thread_id)
    }
