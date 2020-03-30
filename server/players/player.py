from __future__ import annotations


class Player:
    def __init__(self, name: str):
        self._name = name
        self._card = None

    def set_card(self, card: Card) -> None:
        self._card = card

    @property
    def name(self) -> str:
        return self._name

    @property
    def card(self) -> Card:
        return self._card
