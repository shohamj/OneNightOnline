from __future__ import annotations

from abc import ABCMeta, abstractmethod


class Card(metaclass=ABCMeta):
    @abstractmethod
    async def play(self, game: OneNightGame):
        pass
