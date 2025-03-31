from pydantic import BaseModel as PydanticBaseModel
from typing import Any


class BaseModel(PydanticBaseModel):
    pass


class CustomResponse(BaseModel):
    code: int
    message: str
    data: dict | list | None
