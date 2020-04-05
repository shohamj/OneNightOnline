from __future__ import annotations

from abc import ABCMeta, abstractmethod


class Card(metaclass=ABCMeta):
    NUM_OF_VOTES = 1

    @classmethod
    def get_types(cls):
        return [cls.__name__]

    @classmethod
    def should_wake_up(cls, io: GameIO, state: State) -> bool:
        return any(any(card_type in card.get_types() for card_type in cls.get_types()) for card in state.cards)

    @classmethod
    def is_winner(cls, io: GameIO, state: State) -> bool:
        return False

    @classmethod
    async def on_night(cls, io: GameIO, state: State) -> None:
        pass

    @classmethod
    async def on_death(cls, io: GameIO, state: State) -> None:
        pass

    @classmethod
    async def on_win(cls, io: GameIO, state: State) -> None:
        pass
