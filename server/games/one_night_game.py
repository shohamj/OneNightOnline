from __future__ import annotations

import random
from abc import abstractmethod
from typing import List

from server.exceptions.one_night_exception import OneNightException

NUM_OF_CENTER_CARDS = 3


class OneNightGame:

    def __init__(self, players: List[Player], cards: List[Card], action_manager: ActionManager) -> None:
        if len(players) + NUM_OF_CENTER_CARDS != len(cards):
            raise OneNightException(f"Can't create a game with {len(players)} players and {len(cards)} cards")
        self._players = players
        self._cards = cards
        self._center_cards = []
        self._action_manager = action_manager

    @property
    @abstractmethod
    def cards(self) -> List[Card]:
        return []

    @property
    def action_manager(self) -> ActionManager:
        return self._action_manager

    @property
    def players(self) -> List[Player]:
        return self._players

    def hand_out_cards(self) -> None:
        random.shuffle(self._cards)
        self._center_cards = self._cards[:NUM_OF_CENTER_CARDS]
        players_cards = self._cards[NUM_OF_CENTER_CARDS:]
        for player, card in zip(self._players, players_cards):
            player.set_card(card)

    def vote(self, player: Player, votes: List[Player]) -> None:
        self._action_manager.vote(player, votes)

    async def run(self) -> None:
        self.hand_out_cards()
        for card in self.cards:
            await card.play(self)
        most_voted = await self._action_manager.get_most_voted(self._players)
        await self._action_manager.notify_most_voted(most_voted, self._players)
