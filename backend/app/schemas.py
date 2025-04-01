from pydantic import BaseModel as PydanticBaseModel
from typing import Any
from typing import TypeVar, Generic, Union


class BaseModel(PydanticBaseModel):
    pass


T = TypeVar("T")


class CustomResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Union[T, None]
