from typing import Generic, TypeVar, Union

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    pass


T = TypeVar("T")


class CustomResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Union[T, None]
