from typing import List

from server.actions.actions_manager import ActionManager
from server.cards.card import Card
from server.players.player import Player


class OneNightGame:
    def __init__(self, cards: List[Card], players: List[Player], action_manager: ActionManager):
        self._cards = cards
        self._players = players
        self._action_manager = action_manager

    def run(self):
        pass
