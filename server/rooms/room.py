from typing import List

from server.cards.card import Card
from server.players.player import Player


class Room:
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def join(self, player: Player):
        pass
