from random import randint
from typing import List
from socketio import AsyncServer

from server.actions.scoketio_actions_manager import SocketIOActionManager
from server.cards.card import Card
from server.exceptions.one_night_exception import OneNightException
from server.players.player import Player
from server.rooms.room import Room

ERROR_NOT_ROOM_OWNER = "Only the room's owner can start the game"
ERROR_ROOM_NOT_FOUND_ERROR = "Room ID not found"
ERROR_PLAYER_NOT_CREATED_ERROR = "A player must be created before adding or joining rooms"
ERROR_PLAYER_ALREADY_IN_ROOM = "Player has already joined a room"
ERROR_PLAYER_NOT_IN_ROOM = "Player is not in a room"


def generate_room_id(length: int = 6) -> str:
    return "".join([str(randint(0, 9)) for _ in range(length)])


class RoomsManager:
    def __init__(self, server: AsyncServer):
        self.server = server
        self.rooms = {}
        self.sid_to_player = {}
        self.player_to_sid = {}

    def get_player_room(self, sid):
        player = self.sid_to_player[sid]
        for room in self.rooms.values():
            if room.is_member(player):
                return room

    async def create_player(self, sid: str, name: str) -> None:
        if sid in self.sid_to_player:
            raise OneNightException("Player already exists")
        player = Player(name)
        self.sid_to_player[sid] = player
        self.player_to_sid[player] = sid
        await self.server.emit("player_created", {"name": name}, room=sid)

    async def add_room(self, sid: str, cards: List[Card]):
        if sid not in self.sid_to_player:
            raise OneNightException(ERROR_PLAYER_NOT_CREATED_ERROR)
        if self.get_player_room(sid):
            raise OneNightException(ERROR_PLAYER_ALREADY_IN_ROOM)
        player = self.sid_to_player[sid]
        room = Room(player, cards)
        room_id = generate_room_id()
        self.rooms[room_id] = room
        room.join(player)
        await self.server.emit("room_created", {"room_id": room_id}, room=sid)

    async def join_room(self, sid, room_id) -> None:
        if sid not in self.sid_to_player:
            raise OneNightException(ERROR_PLAYER_NOT_CREATED_ERROR)
        if self.get_player_room(sid):
            raise OneNightException(ERROR_PLAYER_ALREADY_IN_ROOM)
        if room_id not in self.rooms:
            raise OneNightException(ERROR_ROOM_NOT_FOUND_ERROR)
        room = self.rooms[room_id]
        new_player = self.sid_to_player[sid]
        room.join(new_player)
        for player in room.players:
            player_sid = self.player_to_sid[player]
            print(player_sid)
            await self.server.emit("player_joined", {"name": new_player.name}, room=player_sid)

    async def exit_room(self, sid, room_id):
        pass

    async def start_game(self, sid):
        if sid not in self.sid_to_player:
            raise OneNightException(ERROR_PLAYER_NOT_CREATED_ERROR)
        room = self.get_player_room(sid)
        if not room:
            raise OneNightException(ERROR_PLAYER_NOT_IN_ROOM)
        if room.owner != self.sid_to_player[sid]:
            raise OneNightException(ERROR_NOT_ROOM_OWNER)
        for player in room.players:
            player_sid = self.player_to_sid[player]
            await self.server.emit("game_started", {}, room=player_sid)
        room.set_action_manager(SocketIOActionManager(self.server, self.sid_to_player, self.player_to_sid))
        await room.start_game()


if __name__ == '__main__':
    print(generate_room_id())
