import json
import logging
from functools import wraps
from json import JSONDecodeError
from typing import Callable

from socketio import AsyncServer

from server.exceptions.one_night_exception import OneNightException

one_night_logger = logging.getLogger("one_night")
one_night_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
one_night_logger.addHandler(handler)


def logger(event_handler: Callable):
    @wraps(event_handler)
    async def decorated_event_handler(sid, data):
        event_name = event_handler.__name__
        one_night_logger.info(f"Event '{event_name}' was called by the client '{sid}' with the data {data}")
        try:
            await event_handler(sid, data)
        except Exception as ex:
            one_night_logger.error(f"Event '{event_name}' raised '{ex}'")
            raise

    return decorated_event_handler


def emit_errors(server: AsyncServer):
    def decorator(event_handler: Callable):
        @wraps(event_handler)
        async def decorated_event_handler(sid, data):
            try:
                await event_handler(sid, data)
            except OneNightException as ex:
                await server.emit("error", {"message": str(ex)}, room=sid)
                raise

        return decorated_event_handler

    return decorator
