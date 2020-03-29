from typing import Dict

import socketio
from aiohttp import web

from server.cards.alien import Alien
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
async def connect(sid: str, environ):
    await sio.emit("message", "Welcome to OneNightOnline", room=sid)


@sio.event
@logger
@emit_errors(sio)
async def create_player(sid: str, data: Dict[str, str]):
    await rooms_manager.create_player(sid, data["name"])


@sio.event
@logger
@emit_errors(sio)
async def add_room(sid: str, data: Dict[str, str]):
    await rooms_manager.add_room(sid, [STR_TO_CARD[card]() for card in data["cards"]])


@sio.event
@logger
@emit_errors(sio)
async def join_room(sid: str, data: Dict[str, str]):
    room_id = data["room_id"]
    await rooms_manager.join_room(sid, room_id)


@sio.event
@logger
@emit_errors(sio)
async def start_game(sid: str, data: Dict[str, str]):
    await rooms_manager.start_game(sid)


@sio.event
@logger
@emit_errors(sio)
async def answer(sid: str, data: Dict[str, str]):
    question_id = data["question_id"]
    user_answer = data["user_answer"]
    print(f"Answer '{user_answer}' for question ID'{question_id}'")


def main():
    web.run_app(app)
