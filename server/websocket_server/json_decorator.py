import json
from functools import wraps
from json import JSONDecodeError


def json_event(event_handler):
    @wraps(event_handler)
    async def decorated_event_handler(sid, data):
        try:
            data_as_json = json.loads(data)
            await event_handler(sid, data_as_json)
        except JSONDecodeError as ex:
            raise AttributeError("Data must be in JSON format") from ex

    return decorated_event_handler
