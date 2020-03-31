from __future__ import annotations

from abc import ABCMeta, abstractmethod

DEFAULT_NUM_OF_VOTES = 1


class Card(metaclass=ABCMeta):
    @property
    def num_of_votes(self):
        return DEFAULT_NUM_OF_VOTES

    @abstractmethod
    async def play(self, game: OneNightGame) -> None:
        pass
