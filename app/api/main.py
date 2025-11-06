from fastapi import APIRouter
from app.api.routes import investment_movement, investment_record, predict, upload

api_router = APIRouter()
api_router.include_router(investment_movement.router)
api_router.include_router(investment_record.router)
api_router.include_router(predict.router)
api_router.include_router(upload.router)
