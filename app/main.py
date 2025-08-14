from app.controllers.hello_controller import router as hello_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(hello_router)
