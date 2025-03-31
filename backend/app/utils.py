from fastapi.responses import ORJSONResponse


# Used for return data structure
def final_response(
    status_code: int,
    message: str | list | None = None,
    data: dict | list | None = None,
) -> dict:
    return {
        "code": status_code,
        "message": message,
        "data": data,
    }


# Used for error responses
def error_response(status_code: int, message: str | list | None = None):
    return ORJSONResponse(
        content=final_response(status_code, message), status_code=status_code
    )


# Used for Swagger docs
def response_model(
    description: str,
    status_code: int,
    message: str | list | None = None,
    data: dict | list | None = None,
):
    return {
        "description": description,
        "content": {
            "application/json": {"example": final_response(status_code, message, data)}
        },
    }
