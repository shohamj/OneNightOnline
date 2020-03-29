from typing import List

from server.actions.actions_manager import ActionManager
from server.cards.card import Card
from server.games.one_night_alien import OneNightAlien
from server.players.player import Player


class Room:
    def __init__(self, owner: Player, cards: List[Card]):
        self._cards = cards
        self._owner = owner
        self._players = []
        self._action_manager = None

    def join(self, player: Player) -> None:
        self._players.append(player)

    def is_member(self, player: Player) -> bool:
        return player in self._players

    def set_action_manager(self, action_manager: ActionManager):
        self._action_manager = action_manager

    @property
    def owner(self) -> Player:
        return self._owner

    @property
    def players(self) -> List[Player]:
        return self._players

    async def start_game(self):
        game = OneNightAlien(self._players, self._cards, self._action_manager)
        await game.run()
