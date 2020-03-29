from typing import List
from socketio import AsyncServer

from server.actions.actions_manager import ActionManager
from server.players.player import Player


class SocketIOActionManager(ActionManager):
    def __init__(self, socket_io_server: AsyncServer, socket_to_player, player_to_socket):
        self._socket_io_server = socket_io_server
        self._socket_to_player = socket_to_player
        self._player_to_socket = player_to_socket

    async def send_message(self, message: str, players: List[Player]):
        for player in players:
            await self._socket_io_server.emit("message", {"message": message}, room=self._player_to_socket[player])
