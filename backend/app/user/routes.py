from fastapi import APIRouter, status
from app.user.deps import ProfileDep

from app.schemas import CustomResponse
from app.user.schemas import ProfileOut

user_router = APIRouter(tags=["User"])


@user_router.get("/profile", response_model=CustomResponse[ProfileOut])
async def get_profile(
    profile: ProfileDep,
):
    return CustomResponse(
        code=status.HTTP_200_OK,
        message="Success",
        data=profile,
    )
