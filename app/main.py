from app.controllers.hello_controller import router as hello_router
from app.controllers.agent_controller import router as agent_router
from fastapi import FastAPI
from app.config.dbconfig import db_create_tables

db_create_tables()  # Create database tables at startup

app = FastAPI()

app.include_router(hello_router)
app.include_router(agent_router, prefix="/agents")
