from server.cards.card import Card


class Player:
    def __init__(self, name: str):
        self._name = name
        self._card = None

    def set_card(self, card: Card) -> None:
        self._card = card

    @property
    def card(self):
        if not self._card:
            raise AttributeError("Player card is not set")

        return self._card

    @property
    def name(self):
        return self._name
