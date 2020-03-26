from server.players.player import Player


class OneNightAlienPlayer(Player):

    def __init__(self, name: str):
        super(OneNightAlienPlayer, self).__init__(name)
        self._index = None

    def set_index(self, index: int):
        self._index = index

    @property
    def index(self):
        if not self._index:
            raise AttributeError("Player index is not set")

        return self._index
