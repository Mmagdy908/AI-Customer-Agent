from fastapi import APIRouter, Request
from app.services.agent_service import send_agent_prompt
from app.models.prompt import Prompt

router = APIRouter()


@router.post("/", status_code=200)
async def send_prompt(prompt: Prompt):
    return {"response": send_agent_prompt(prompt.content, prompt.thread_id)}
