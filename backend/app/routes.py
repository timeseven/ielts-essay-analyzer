from fastapi import APIRouter

from app.auth.routes import auth_router
from app.client.routes import client_router

api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(client_router, prefix="/client/{client_id}")
