from random import randint
from typing import List
from engineio import AsyncServer

from server.cards.card import Card
from server.exceptions.one_night_exception import OneNightException
from server.players.player import Player
from server.rooms.room import Room

PLAYER_NOT_CREATED_ERROR = "A player must be created before adding or joining rooms"
PLAYER_ALREADY_IN_ROOM_ERROR = "Player has already joined a room"


def generate_room_id(length: int = 6) -> str:
    return "".join([str(randint(0, 9)) for _ in range(length)])


class RoomsManager:
    def __init__(self, server: AsyncServer):
        self.server = server
        self.rooms = {}
        self.sid_to_player = {}
        self.player_to_sid = {}

    def is_player_in_room(self, sid) -> bool:
        player = self.sid_to_player[sid]
        return any([room.is_member(player) for room in self.rooms.values()])

    def create_player(self, sid: str, name: str) -> None:
        if sid in self.sid_to_player:
            raise OneNightException("Player already exists")

        player = Player(name)
        self.sid_to_player[sid] = player
        self.player_to_sid[player] = sid

    def add_room(self, sid: str, cards: List[Card]) -> str:
        if sid not in self.sid_to_player:
            raise OneNightException(PLAYER_NOT_CREATED_ERROR)
        if self.is_player_in_room(sid):
            raise OneNightException(PLAYER_ALREADY_IN_ROOM_ERROR)
        room = Room(cards)
        room_id = generate_room_id()
        self.rooms[room_id] = room
        room.join(self.sid_to_player[sid])
        return room_id

    def join_room(self, sid, room_id) -> None:
        if sid not in self.sid_to_player:
            raise OneNightException(PLAYER_NOT_CREATED_ERROR)
        if self.sid_to_player[sid].room:
            raise OneNightException(PLAYER_ALREADY_IN_ROOM_ERROR)
        self.rooms[room_id].join(self.sid_to_player[sid])

    def exit_room(self, sid, room_id):
        pass

    def start_game(self, sid, room_id):
        pass


if __name__ == '__main__':
    print(generate_room_id())
