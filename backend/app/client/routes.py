from fastapi import APIRouter

from app.user.routes import user_router

client_router = APIRouter()


client_router.include_router(user_router, prefix="/user")
