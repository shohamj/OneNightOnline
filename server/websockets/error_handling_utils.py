from __future__ import annotations

from functools import wraps
from typing import Callable

from server.exceptions.one_night_exception import OneNightException


def emit_errors(server: AsyncServer) -> Callable:
    def decorator(event_handler: Callable) -> Callable:
        @wraps(event_handler)
        async def decorated_event_handler(sid, data) -> None:
            try:
                await event_handler(sid, data)
            except OneNightException as ex:
                await server.emit("error", {"message": str(ex)}, room=sid)
                raise

        return decorated_event_handler

    return decorator
