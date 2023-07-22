from typing import Any

from backend.app.models import Response


def _send_error(msg: str) -> Response:
    return Response(
        status_code=404,
        response_type="error",
        description=msg,
        data=None,
    )


def _send_data(data: Any) -> Response:
    return Response(
        status_code=200,
        response_type="success",
        description="Operation successful",
        data=data
    )
