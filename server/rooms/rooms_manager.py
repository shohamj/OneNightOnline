from __future__ import annotations

from random import randint
from typing import List

from server.actions.scoketio_actions_manager import SocketIOActionManager
from server.exceptions.one_night_exception import OneNightException
from server.io.socket_game_io import SocketGameIO
from server.players.player import Player
from server.rooms.room import Room

ERROR_PLAYER_ALREADY_EXISTS = "Player already exists"
ERROR_NOT_ROOM_OWNER = "Only the room's owner can start the game"
ERROR_ROOM_NOT_FOUND_ERROR = "Room ID not found"
ERROR_PLAYER_NOT_CREATED_ERROR = "Player doesn't exist"
ERROR_PLAYER_ALREADY_IN_ROOM = "Player has already joined a room"
ERROR_PLAYER_NOT_IN_ROOM = "Player is not in a room"


def generate_room_id(length: int = 6) -> str:
    return "".join([str(randint(0, 9)) for _ in range(length)])


class RoomsManager:
    def __init__(self, server: AsyncServer) -> None:
        self.server = server
        self.rooms = {}
        self._sid_to_player = {}
        self._player_to_sid = {}

    def player_exists(self, sid: str) -> bool:
        return sid in self._sid_to_player

    def get_player_room(self, sid: str) -> Room:
        player = self._sid_to_player[sid]
        for room in self.rooms.values():
            if room.is_member(player):
                return room

    async def create_player(self, sid: str, name: str) -> None:
        if self.player_exists(sid):
            raise OneNightException(ERROR_PLAYER_ALREADY_EXISTS)
        player = Player(name)
        self._sid_to_player[sid] = player
        self._player_to_sid[player] = sid
        await self.server.emit("player_created", {"name": player.name, "id": player.id}, room=sid)

    async def add_room(self, sid: str, cards: List[Card]) -> None:
        if not self.player_exists(sid):
            raise OneNightException(ERROR_PLAYER_NOT_CREATED_ERROR)
        if self.get_player_room(sid):
            raise OneNightException(ERROR_PLAYER_ALREADY_IN_ROOM)
        player = self._sid_to_player[sid]
        room = Room(player, cards)
        room_id = generate_room_id()
        self.rooms[room_id] = room
        room.join(player)
        await self.server.emit("room_created", {"room_id": room_id}, room=sid)

    async def join_room(self, sid: str, room_id: str) -> None:
        if not self.player_exists(sid):
            raise OneNightException(ERROR_PLAYER_NOT_CREATED_ERROR)
        if self.get_player_room(sid):
            raise OneNightException(ERROR_PLAYER_ALREADY_IN_ROOM)
        if room_id not in self.rooms:
            raise OneNightException(ERROR_ROOM_NOT_FOUND_ERROR)
        room = self.rooms[room_id]
        new_player = self._sid_to_player[sid]
        room.join(new_player)
        for player in room.players:
            player_sid = self._player_to_sid[player]
            await self.server.emit("player_joined", {"name": new_player.name, "id": new_player.id}, room=player_sid)

    async def leave_room(self, sid: str) -> None:
        if not self.player_exists(sid):
            raise OneNightException(ERROR_PLAYER_NOT_CREATED_ERROR)
        room = self.get_player_room(sid)
        if not room:
            raise OneNightException(ERROR_PLAYER_NOT_IN_ROOM)
        leaving_player = self._sid_to_player[sid]
        room.leave(leaving_player)
        for player in room.players:
            player_sid = self._player_to_sid[player]
            await self.server.emit("player_left", {"name": leaving_player.name, "id": leaving_player.id},
                                   room=player_sid)

    async def start_game(self, sid: str) -> None:
        if not self.player_exists(sid):
            raise OneNightException(ERROR_PLAYER_NOT_CREATED_ERROR)
        room = self.get_player_room(sid)
        if not room:
            raise OneNightException(ERROR_PLAYER_NOT_IN_ROOM)
        if room.owner != self._sid_to_player[sid]:
            raise OneNightException(ERROR_NOT_ROOM_OWNER)
        for player in room.players:
            player_sid = self._player_to_sid[player]
            await self.server.emit("game_started", {}, room=player_sid)
        room.set_game_io(SocketGameIO())
        await room.start_game()

    def vote(self, sid: str, players_ids: List[str]):
        if not self.player_exists(sid):
            raise OneNightException(ERROR_PLAYER_NOT_CREATED_ERROR)
        room = self.get_player_room(sid)
        if not room:
            raise OneNightException(ERROR_PLAYER_NOT_IN_ROOM)
        voted_players = [player for player in room.players if player.id in players_ids]
        voting_player = self._sid_to_player[sid]
        room.game.vote(voting_player, voted_players)


if __name__ == '__main__':
    print(generate_room_id())
