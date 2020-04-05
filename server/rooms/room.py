from __future__ import annotations

from typing import List

from server.game.one_night_alien import OneNightAlien


class Room:
    def __init__(self, owner: Player, cards: List[Card]) -> None:
        self._cards = cards
        self._owner = owner
        self._players = []
        self._game_io = None
        self._game = None

    def join(self, player: Player) -> None:
        self._players.append(player)

    def leave(self, player: Player) -> None:
        self._players.remove(player)

    def is_member(self, player: Player) -> bool:
        return player in self._players

    def set_game_io(self, action_manager: ActionManager) -> None:
        self._game_io = action_manager

    @property
    def owner(self) -> Player:
        return self._owner

    @property
    def players(self) -> List[Player]:
        return self._players

    @property
    def game(self) -> OneNightGame:
        return self._game

    async def start_game(self) -> None:
        self._game = OneNightAlien(self._players, self._cards, self._game_io)
        await self._game.run()
