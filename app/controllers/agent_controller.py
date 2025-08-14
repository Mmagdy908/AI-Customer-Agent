from fastapi import APIRouter
from app.services.agent_service import send_agent_prompt

router = APIRouter()


@router.post("/prompts", response_model=dict[str, str], status_code=200)
def send_prompt():
    print("HELLLOO")
    return {"response": send_agent_prompt("prompt")}
