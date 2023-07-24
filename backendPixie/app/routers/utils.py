from typing import Any

from app.schemas import Response


def send_error(msg: str) -> Response:
    return Response(
        status_code=404,
        response_type="error",
        description=msg,
        data=None,
    )


def send_data(data: Any) -> Response:
    return Response(
        status_code=200,
        response_type="success",
        description="Operation successful",
        data=data
    )
