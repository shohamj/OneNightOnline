from typing import List

from server.cards.alien import Alien
from server.cards.card import Card
from server.games.one_night_game import OneNightGame


class OneNightAlien(OneNightGame):
    @property
    def cards(self) -> List[Card]:
        return [Alien()]
