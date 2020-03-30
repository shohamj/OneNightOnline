from typing import Dict

import socketio
from aiohttp import web

from server.cards.alien import Alien
from server.exceptions.one_night_exception import OneNightException
from server.rooms.rooms_manager import RoomsManager
from server.websocket_server.decorators import logger, emit_errors

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)
rooms_manager = RoomsManager(sio)

STR_TO_CARD = {
    "alien": Alien
}


@sio.event
@logger
async def connect(sid: str, environ: Dict[str, str]) -> None:
    await sio.emit("message", {"message": "Welcome to OneNightOnline"}, room=sid)


@sio.event
@logger
async def disconnect(sid: str) -> None:
    if rooms_manager.player_exists(sid) and rooms_manager.get_player_room(sid):
        await rooms_manager.leave_room(sid)


@sio.event
@logger
@emit_errors(sio)
async def create_player(sid: str, data: Dict[str, str]) -> None:
    await rooms_manager.create_player(sid, data["name"])


@sio.event
@logger
@emit_errors(sio)
async def add_room(sid: str, data: Dict[str, str]) -> None:
    await rooms_manager.add_room(sid, [STR_TO_CARD[card]() for card in data["cards"]])


@sio.event
@logger
@emit_errors(sio)
async def join_room(sid: str, data: Dict[str, str]) -> None:
    if "room_id" not in data:
        raise OneNightException("Missing key 'room_id")
    room_id = data["room_id"]
    await rooms_manager.join_room(sid, room_id)


@sio.event
@logger
@emit_errors(sio)
async def exit_room(sid: str, data: Dict[str, str]) -> None:
    if "room_id" not in data:
        raise OneNightException("Missing key 'room_id")
    room_id = data["room_id"]
    await rooms_manager.leave_room(sid, room_id)


@sio.event
@logger
@emit_errors(sio)
async def start_game(sid: str, data: Dict[str, str]) -> None:
    await rooms_manager.start_game(sid)


@sio.event
@logger
@emit_errors(sio)
async def answer(sid: str, data: Dict[str, str]) -> None:
    if "question_id" not in data:
        raise OneNightException("Missing key 'question_id")
    if "user_answer" not in data:
        raise OneNightException("Missing key 'user_answer")
    question_id = data["question_id"]
    user_answer = data["user_answer"]
    print(f"Answer '{user_answer}' for question ID'{question_id}'")


def main():
    web.run_app(app)
