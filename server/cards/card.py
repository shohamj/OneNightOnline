from __future__ import annotations

from abc import ABCMeta, abstractmethod

DEFAULT_NUM_OF_VOTES = 1


class Card(metaclass=ABCMeta):
    NUM_OF_VOTES = 1

    @staticmethod
    def get_num_of_votes():
        return DEFAULT_NUM_OF_VOTES

    @classmethod
    def main_type(cls):
        return cls.__name__

    @classmethod
    def sub_types(cls):
        return []

    @classmethod
    def get_types(cls):
        return [cls.main_type(), *cls.sub_types()]

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
