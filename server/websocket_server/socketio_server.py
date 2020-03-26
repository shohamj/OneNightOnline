import socketio
from aiohttp import web

from server.websocket_server.json_decorator import json_event

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    print("New connection")
    await sio.emit("message", "Welcome to OneNightOnline")


@sio.event
@json_event
async def add_room(sid, data):
    if "room_name" not in data:
        raise ValueError("Missing key 'room_key'")
    room_name = data["room_name"]
    print(f"Adding room '{room_name}'")


@sio.event
@json_event
async def join_room(sid, data):
    if "room_id" not in data:
        raise ValueError("Missing key 'room_id'")
    room_id = data["room_id"]
    print(f"Joining room '{room_id}'")


@sio.event
@json_event
async def start_game(sid, data):
    if "room_id" not in data:
        raise ValueError("Missing key 'room_id'")
    room_id = data["room_id"]
    print(f"Starting game for room '{room_id}'")


@sio.event
@json_event
async def answer(sid, data):
    if "question_id" not in data:
        raise ValueError("Missing key 'question_id'")
    if "user_answer" not in data:
        raise ValueError("Missing key 'user_answer'")
    question_id = data["question_id"]
    user_answer = data["user_answer"]
    print(f"Answer '{user_answer}' for question ID'{question_id}'")


@sio.event
@json_event
async def set_name(sid, data):
    if "name" not in data:
        raise ValueError("Missing key 'name'")
    name = data["name"]
    print(f"Setting name '{name}'")


def main():
    web.run_app(app)
