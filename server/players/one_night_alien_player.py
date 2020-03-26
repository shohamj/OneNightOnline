from server.players.player import Player


class OneNightAlienPlayer(Player):

    def __init__(self, name: str):
        super(OneNightAlienPlayer, self).__init__(name)
        self._index = None

    def set_index(self, index: int) -> None:
        self._index = index

    @property
    def index(self) -> int:
        return self._index
