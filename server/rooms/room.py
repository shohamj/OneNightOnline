from typing import List

from server.cards.card import Card
from server.players.player import Player


class Room:
    def __init__(self, cards: List[Card]):
        self.cards = cards
        self.players = []

    def join(self, player: Player) -> None:
        self.players.append(player)

    def is_member(self, player: Player) -> bool:
        return player in self.players
