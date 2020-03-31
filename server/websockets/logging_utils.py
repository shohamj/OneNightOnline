from __future__ import annotations

import logging
from functools import wraps
from typing import Callable

one_night_logger = logging.getLogger("one_night")
one_night_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
one_night_logger.addHandler(handler)


def logger(event_handler: Callable) -> Callable:
    @wraps(event_handler)
    async def decorated_event_handler(*args: any) -> None:
        event_name = event_handler.__name__
        if len(args) == 2:
            sid, data = args
        else:
            sid = args[0]
            data = None
        one_night_logger.info(f"Received event '{event_name}' from the client '{sid}' with the data {data}")
        try:
            await event_handler(*args)
        except Exception as ex:
            one_night_logger.error(f"Event '{event_name}' raised '{ex}'")
            raise

    return decorated_event_handler


def emit_with_logs(original_emit):
    async def emit(*args, **kwargs):
        event = args[0]
        data = args[1]
        sid = kwargs["room"]
        one_night_logger.info(f"Emitted event '{event}' to the client '{sid}' with the data {data}")
        return await original_emit(*args, **kwargs)

    return emit
