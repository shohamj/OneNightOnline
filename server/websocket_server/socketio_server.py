from typing import Dict

import socketio
from aiohttp import web

from server.rooms.rooms_manager import RoomsManager
from server.websocket_server.decorators import json_data, logger

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)
rooms_manager = RoomsManager(sio)


@sio.event
@logger
async def connect(sid: str, environ):
    await sio.emit("message", "Welcome to OneNightOnline")


@sio.event
@logger
@json_data
async def create_player(sid: str, data: Dict[str, str]):
    rooms_manager.create_player(sid, data["name"])


@sio.event
@logger
@json_data
async def add_room(sid: str, data: Dict[str, str]):
    rooms_manager.add_room(sid, [])


@sio.event
@logger
@json_data
async def join_room(sid: str, data: Dict[str, str]):
    room_id = data["room_id"]
    print(f"Joining room '{room_id}'")


@sio.event
@logger
@json_data
async def start_game(sid: str, data: Dict[str, str]):
    room_id = data["room_id"]
    print(f"Starting game for room '{room_id}'")


@sio.event
@logger
@json_data
async def answer(sid: str, data: Dict[str, str]):
    question_id = data["question_id"]
    user_answer = data["user_answer"]
    print(f"Answer '{user_answer}' for question ID'{question_id}'")


@sio.event
@logger
@json_data
async def set_name(sid: str, data: dict):
    name = data["name"]
    print(f"Setting name '{name}'")


def main():
    web.run_app(app)
