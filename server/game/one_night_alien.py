from __future__ import annotations

from typing import List

from server.cards.alien import Alien
from server.game.one_night_game import OneNightGame


class OneNightAlien(OneNightGame):
    @property
    def night_order(self) -> List[Card]:
        return [Alien]
