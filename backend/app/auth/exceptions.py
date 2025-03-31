from typing import Any

from fastapi import HTTPException, status


class AuthHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(
        self, status_code: int = None, detail: str = None, **kwargs: dict[str, Any]
    ) -> None:
        super().__init__(
            status_code=status_code or self.STATUS_CODE,
            detail=detail or self.DETAIL,
            **kwargs,
        )


class NotAuthenticated(AuthHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Not authenticated"
