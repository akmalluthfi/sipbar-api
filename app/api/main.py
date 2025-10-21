from fastapi import APIRouter
from app.api.routes import investment_movement, investment_record

api_router = APIRouter()
api_router.include_router(investment_movement.router)
api_router.include_router(investment_record.router)
