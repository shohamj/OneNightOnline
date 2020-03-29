from abc import ABCMeta, abstractmethod

import server.games.one_night_game as one_night_game


class Card(metaclass=ABCMeta):

    @abstractmethod
    async def play(self, game: one_night_game.OneNightGame):
        pass
