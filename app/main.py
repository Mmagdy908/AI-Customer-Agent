from app.controllers.hello_controller import router as hello_router
from app.controllers.agent_controller import router as agent_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(hello_router)
app.include_router(agent_router, prefix="/agents")
