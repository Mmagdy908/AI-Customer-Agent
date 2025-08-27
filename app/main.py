from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.hello_controller import router as hello_router
from app.controllers.thread_controller import router as thread_router
from app.controllers.message_controller import router as message_router
from app.controllers.auth_controller import router as auth_router
from app.config.dbconfig import db_create_tables


db_create_tables()  # Create database tables at startup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hello_router)
app.include_router(thread_router, prefix="/api/v1/threads")
app.include_router(message_router, prefix="/api/v1/messages")
app.include_router(auth_router, prefix="/api/v1/auth")
