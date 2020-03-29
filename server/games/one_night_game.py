import random
from abc import abstractmethod
from typing import List

from server.actions.actions_manager import ActionManager
from server.exceptions.one_night_exception import OneNightException

NUM_OF_CENTER_CARDS = 3


class OneNightGame:

    def __init__(self, players, cards, action_manager):
        if len(players) + NUM_OF_CENTER_CARDS != len(cards):
            raise OneNightException(f"Can't create a game with {len(players)} players and {len(cards)} cards")
        self._players = players
        self._cards = cards
        self._center_cards = []
        self._action_manager = action_manager

    @property
    @abstractmethod
    def cards(self):
        return []

    @property
    def action_manager(self) -> ActionManager:
        return self._action_manager

    @property
    def players(self):
        return self._players

    def hand_out_cards(self):
        random.shuffle(self._cards)
        self._center_cards = self._cards[:NUM_OF_CENTER_CARDS]
        players_cards = self._cards[NUM_OF_CENTER_CARDS:]
        for player, card in zip(self._players, players_cards):
            player.set_card(card)

    async def run(self) -> None:
        self.hand_out_cards()
        for card in self.cards:
            await card.play(self)
