from fastapi import APIRouter
from app.api.routes import hello

api_router = APIRouter()
api_router.include_router(hello.router)
