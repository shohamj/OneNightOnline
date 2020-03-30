from __future__ import annotations

import uuid


class Player:
    def __init__(self, name: str) -> None:
        self._name = name
        self._card = None
        self._id = uuid.uuid4().hex

    def set_card(self, card: Card) -> None:
        self._card = card

    @property
    def name(self) -> str:
        return self._name

    @property
    def card(self) -> Card:
        return self._card

    @property
    def id(self) -> str:
        return self._id
