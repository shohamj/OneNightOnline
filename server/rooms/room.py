from __future__ import annotations

from typing import List

from server.games.one_night_alien import OneNightAlien


class Room:
    def __init__(self, owner: Player, cards: List[Card]) -> None:
        self._cards = cards
        self._owner = owner
        self._players = []
        self._action_manager = None

    def join(self, player: Player) -> None:
        self._players.append(player)

    def leave(self, player: Player) -> None:
        self._players.remove(player)

    def is_member(self, player: Player) -> bool:
        return player in self._players

    def set_action_manager(self, action_manager: ActionManager) -> None:
        self._action_manager = action_manager

    @property
    def owner(self) -> Player:
        return self._owner

    @property
    def players(self) -> List[Player]:
        return self._players

    async def start_game(self) -> None:
        game = OneNightAlien(self._players, self._cards, self._action_manager)
        await game.run()
