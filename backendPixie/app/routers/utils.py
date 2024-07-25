from typing import Any
from fastapi.responses import JSONResponse

from app.schemas import Response


# def send_error(msg: str) -> Response:
#     return Response(
#         status_code=404,
#         response_type="error",
#         description=msg,
#         data=None,
#     )

def send_error(message: str, status_code: int = 400):
    return JSONResponse(
        status_code=status_code, 
        content={
            "response_type": "error", 
            "description": message
            }
        )

def send_data(data: Any) -> Response:
    return Response(
        status_code=200,
        response_type="success",
        description="Operation successful",
        data=data
    )
