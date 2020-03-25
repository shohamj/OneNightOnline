import socketio
from aiohttp import web

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    print("New connection")
    await sio.emit("message", "Welcome to OneNightOnline")


if __name__ == '__main__':
    web.run_app(app)
